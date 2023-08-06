from __future__ import absolute_import
from deployer.utils import parse_constraints
import itertools
from jujuclient.exc import (
    UnitErrors,
    EnvError,
)
from six.moves import range


class MemoryEnvironment(object):
    """ In memory deployment: not all features implemented
        (notably subordinates and their relations).
    """

    def __init__(self, name, deployment):
        """ Two main dicts: _services (return-able as part of status(),
            and _services_data (to hold e.g. config, constraints)
        """
        super(MemoryEnvironment, self).__init__()
        self.name = name
        self._deployment = deployment
        self._services = {}
        self._services_data = {}
        self._relations = {}
        self._do_deploy()

    def add_units(self, svc_name, num):
        """Add units
        """
        next_num = self._services_data[svc_name]['next_unit_num']
        for idx in range(next_num, next_num + num):
            self._services[svc_name]['units'].append(
                '{}/{}'.format(svc_name, idx))
        self._services_data[svc_name]['next_unit_num'] = \
            next_num + num

    def remove_unit(self, unit_name):
        """ Remove a unit by name """
        svc_name = unit_name.split('/')[0]
        units_idx = {unit: idx for idx, unit in
                     enumerate(self._services[svc_name]['units'])}
        try:
            self._services[svc_name]['units'].pop(
                units_idx[unit_name])
        except KeyError:
            raise UnitErrors("Invalid unit name")

    def _get_service(self, svc_name):
        """ Get service by name (as returned by status())
        """
        if svc_name not in self._services:
            raise EnvError("Invalid service name")
        return self._services[svc_name]

    def _remove_relation(self, s_from, r_from, s_to):
        """Low level _remove_relation
        """
        rels = self._relations.get(s_from, {})
        related_svcs = rels.get(r_from, [])
        if s_to in related_svcs:
            related_svcs.remove(s_to)

    def remove_relation(self, src_ep, dst_ep):
        """Remove relation, eps are "service_name:rel_name"
        """
        assert ":" in src_ep and ":" in dst_ep
        (svc0, rel0, svc1, rel1) = src_ep.split(':') + dst_ep.split(':')
        for (s_from, r_from, s_to) in ((svc0, rel0, svc1),
                                       (svc1, rel1, svc0)):
            self._remove_relation(s_from, r_from, s_to)

    def _remove_service_relations(self, svc):
        self._relations.pop(svc, None)
        for _, rels in self._relations.items():
            for _, dst_svcs in rels.items():
                while svc in dst_svcs:
                    dst_svcs.remove(svc)

    def _add_relation(self, s_from, r_from, s_to):
        """Low level _add_relation (only one-way)
        """
        src_rels = self._relations.setdefault(s_from, {})
        src_rels.setdefault(r_from, [])
        src_rels[r_from].append(s_to)

    def add_relation(self, src_ep, dst_ep):
        """Add relation, eps are "service_name:rel_name"
        """
        assert ":" in src_ep and ":" in dst_ep
        (svc0, rel0, svc1, rel1) = src_ep.split(':') + dst_ep.split(':')
        for (s_from, r_from, s_to) in ((svc0, rel0, svc1),
                                       (svc1, rel1, svc0)):
            self._add_relation(s_from, r_from, s_to)

    def destroy_service(self, svc_name):
        """ Destroy a service
        """
        if svc_name not in self._services:
            raise EnvError("Invalid service name")
        self._remove_service_relations(svc_name)
        del self._services[svc_name]

    def close(self):
        """
        """

    def connect(self):
        """
        """

    def set_config(self, svc_name, cfg_dict):
        """ Set service config from passed dict, keeping
            the structure as needed for status() return
        """
        config = self.get_config(svc_name)
        if cfg_dict:
            for cfg_k, cfg_v in cfg_dict.items():
                config_entry = config.setdefault(cfg_k, {})
                config_entry['value'] = cfg_v

    def set_constraints(self, svc_name, constr_str):
        """ Set service constraints from "key=value ..."
            passed string
        """
        constraints = parse_constraints(constr_str) if constr_str else {}
        self._services_data[svc_name]['constraints'] = constraints

    def get_config(self, svc_name):
        """ Return service configs - note its structure:
            config{thename: {'value': thevalue}, ...}
        """
        return self._services_data[svc_name]['config']

    def get_constraints(self, svc_name):
        """ Return service constraints dict
        """
        return self._services_data[svc_name]['constraints']

    def get_cli_status(self):
        pass

    def reset(self):
        pass

    def resolve_errors(self, retry_count=0, timeout=600, watch=False, delay=5):
        pass

    def _do_deploy(self):
        """ Fake deploy: build in-memory representation of the deployed set
            of services from deployment
        """
        self._compile_relations()
        for service in self._deployment.get_services():
            svc_name = service.name
            charm = self._deployment.get_charm_for(svc_name)
            relations = self._relations.setdefault(svc_name, {})
            self._services[svc_name] = {
                'units': [],
                'charm': charm.name,
                'relations': relations,
            }
            self._services_data[svc_name] = {
                'next_unit_num': 0,
                'config': {},
                'constraints': {},
            }
            # XXX: Incomplete relations support: only add units for non-subords
            num_units = 0 if charm.is_subordinate() else service.num_units
            self.add_units(svc_name, num_units)
            self.set_config(svc_name, service.config)
            self.set_constraints(svc_name, service.constraints)

    def _get_charm_if_rels_map(self, svc, req_prov):
        """Return a map of interface names to sets of charm relation names.

        req_prov specifies the relation direction (requires if True,
        otherwise provides).

        e.g. {"rabbitmq": {"amqp", "amqp-nova"}, "http": {"website"}}
        """
        charm = self._deployment.get_charm_for(svc)
        try:
            if req_prov:
                charm_relations = charm.get_requires()
            else:
                charm_relations = charm.get_provides()
        except KeyError:
            return {}
        if_rels_map = {}
        for relations in charm_relations.values():
            for relation in relations:
                interface = relation.get('interface')
                names = if_rels_map.setdefault(interface, set())
                names.add(relation.get('name'))
        return if_rels_map

    def _compile_relations(self):
        """Compile the configured relations into status()-compatible format."""
        for rel in self._deployment.get_relations():
            candidates = []
            # Try both directions.
            for src, dst in (rel[0], rel[1]), (rel[1], rel[0]):
                # src, dst are svcname[:relation_name], e.g.:
                # "rabbitmq" or "rabbitmq:amqp"
                src_svc, src_rel = (src + ':').split(':')[:2]
                dst_svc, dst_rel = (dst + ':').split(':')[:2]

                src_charm_if_rels = self._get_charm_if_rels_map(src_svc, 0)
                dst_charm_if_rels = self._get_charm_if_rels_map(dst_svc, 1)

                # Find all possible relations with matching interfaces
                # between the charms, and filter them down based on any
                # provided relation names.
                for src_charm_if, src_charm_rels in src_charm_if_rels.items():
                    dst_charm_rels = dst_charm_if_rels.get(src_charm_if)
                    if not dst_charm_rels:
                        continue

                    # Filter by name if provided.
                    src_rels = [
                        rel for rel in src_charm_rels
                        if src_rel == rel or not src_rel]
                    dst_rels = [
                        rel for rel in dst_charm_rels
                        if dst_rel == rel or not dst_rel]

                    # All remaining combinations are possibilities.
                    candidates.extend([
                        ((src_svc, src_rel), (dst_svc, dst_rel))
                        for src_rel, dst_rel
                        in itertools.product(src_rels, dst_rels)])

            # Check that we found exactly one possible relation.
            # TODO: Better error handling.
            if not candidates:
                raise Exception(
                    "No relations possible for %s <-> %s" % (src, dst))
            elif len(candidates) > 1:
                raise Exception(
                    "Ambiguous relation %s <-> %s: candidates are %s"
                    % (src, dst,
                       ", ".join([
                           "%s:%s <-> %s:%s" % (
                               src_svc, src_rel, dst_svc, dst_rel)
                           for ((src_svc, src_rel), (dst_svc, dst_rel))
                           in candidates])))

            # Add the identified relation to our state.
            [((src_svc, src_rel), (dst_svc, dst_rel))] = candidates
            self._add_relation(src_svc, src_rel, dst_svc)
            self._add_relation(dst_svc, dst_rel, src_svc)

    def status(self):
        """ Return all services status """
        return {'services': self._services}

    def wait_for_units(self, *args, **kwargs):
        pass
