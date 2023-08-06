from __future__ import absolute_import
from __future__ import print_function
import logging
import time

from .base import BaseAction
from ..relation import EndpointPair
from ..utils import parse_constraints, yaml_dump
import six


class Diff(BaseAction):

    log = logging.getLogger("deployer.diff")

    def __init__(self, env, deployment, options):
        self.options = options
        self.env = env
        self.deployment = deployment
        self.env_status = None
        self.env_state = {'services': {}, 'relations': []}

    def load_env(self):
        """
        """
        rels = set()
        for svc_name in self.env_status['services']:
            if svc_name not in self.env_status['services']:
                self.env_state['services'][svc_name] = 'missing'
            self.env_state['services'].setdefault(svc_name, {})[
                'options'] = self.env.get_config(svc_name)
            self.env_state['services'][svc_name][
                'constraints'] = self.env.get_constraints(svc_name)
            self.env_state['services'][svc_name]['unit_count'] = len(
                (self.env_status['services'][svc_name].get('units') or {}))
            rels.update(self._load_rels(svc_name))
        self.env_state['relations'] = sorted(rels)

    def _load_rels(self, svc_name):
        rels = set()
        svc_rels = self.env_status['services'][svc_name].get(
            'relations', {})
        # There is ambiguity here for multiple rels between two
        # services without the relation id, which we need support
        # from core for.
        for r_name, r_svcs in svc_rels.items():
            for r_svc in r_svcs:
                # Skip peer relations
                if r_svc == svc_name:
                    continue
                rr_name = self._get_rel_name(svc_name, r_svc)
                rels.add(
                    tuple(sorted([
                        "%s:%s" % (svc_name, r_name),
                        "%s:%s" % (r_svc, rr_name)])))
        return rels

    def _get_rel_name(self, src, tgt):
        svc_rels = self.env_status['services'][tgt]['relations']
        found = None
        for r, eps in svc_rels.items():
            if src in eps:
                if found:
                    self.deployment.log.warning(
                        "Application: %s will show ambiguous relations to %s"
                        % (src, tgt))
                    # use "*" to note the ambiguity - will be specially
                    # processed by Endpoint comparisons as a kind of
                    # ~wildcard
                    found = "*"
                else:
                    found = r
        return found

    def get_delta(self):
        delta = {}
        rels_delta = self._get_relations_delta()
        if rels_delta:
            delta['relations'] = rels_delta
        svc_delta = self._get_services_delta()
        if svc_delta:
            delta['services'] = svc_delta
        return delta

    def _get_relations_delta(self):
        # Simple endpoint diff, no qualified endpoint checking.

        # Env relations are always qualified (at least in go).
        delta = {}
        env_rels = set(
            EndpointPair(*x) for x in self.env_state.get('relations', ()))
        dep_rels = set(
            [EndpointPair(*y) for y in self.deployment.get_relations()])

        for r in dep_rels.difference(env_rels):
            delta.setdefault('missing', []).append(r)

        for r in env_rels.difference(dep_rels):
            delta.setdefault('unknown', []).append(r)

        return delta

    def _get_services_delta(self):
        delta = {}
        env_svcs = set(self.env_status['services'].keys())
        dep_svcs = set([s.name for s in self.deployment.get_services()])

        missing = dep_svcs - env_svcs
        if missing:
            delta['missing'] = {}
        for a in missing:
            delta['missing'][a] = self.deployment.get_service(
                a).svc_data
        unknown = env_svcs - dep_svcs
        if unknown:
            delta['unknown'] = {}
        for r in unknown:
            delta['unknown'][r] = self.env_state.get(r)

        for cs in env_svcs.intersection(dep_svcs):
            d_s = self.deployment.get_service(cs).svc_data
            e_s = self.env_state['services'][cs]
            mod = self._diff_service(e_s, d_s,
                                     self.deployment.get_charm_for(cs))
            if not mod:
                continue
            if 'modified' not in delta:
                delta['modified'] = {}
            delta['modified'][cs] = mod
        return delta

    def _diff_service(self, env_service, dep_service, charm):
        mod = {}

        # Start by diffing the constraints.
        dep_constraints = parse_constraints(dep_service.get('constraints', ''))
        # 'tags' is a special case, as it can be multi-valued: convert to list
        # if the deployment specifies just a string
        if isinstance(dep_constraints.get('tags'), six.string_types):
            dep_constraints['tags'] = [dep_constraints['tags']]
        if dep_constraints != env_service['constraints']:
            mod['env-constraints'] = env_service['constraints']
            mod['cfg-constraints'] = dep_constraints

        # Now collect all the options from both services and diff them.
        all_options = (set(dep_service.get('options', {}).keys()) |
                       set(env_service.get('options', {}).keys()))
        for key in all_options:
            dep_value = dep_service.get('options', {}).get(key)
            # Assume the charm default if the deployment specifies no value.
            if dep_value is None:
                dep_value = charm.config.get(key, {}).get('default', None)
            env_value = env_service['options'].get(key, {}).get('value')
            if env_value != dep_value:
                mod.setdefault('env-config', {}).update({key: env_value})
                mod.setdefault('cfg-config', {}).update({key: dep_value})

        # Finally, compare the unit counts if appropriate.
        if not charm or not charm.is_subordinate():
            # XXX: The num_units default policy should really be
            # implemented centrally.
            dep_unit_count = dep_service.get('num_units', 1)
            if env_service['unit_count'] != dep_unit_count:
                mod['num_units'] = env_service['unit_count'] - dep_unit_count
        return mod

    def do_diff(self):
        self.start_time = time.time()
        self.deployment.resolve()
        self.env.connect()
        self.env_status = self.env.status()
        self.load_env()
        return self.get_delta()

    def run(self):
        diff = self.do_diff()
        if diff:
            print(yaml_dump(diff))
