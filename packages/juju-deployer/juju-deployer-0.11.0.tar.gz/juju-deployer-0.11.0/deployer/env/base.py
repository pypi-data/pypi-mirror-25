from __future__ import absolute_import
import logging

from ..utils import (
    AlternateKeyDict,
    ErrorExit,
    DeploymentError,
    yaml_load,
    yaml_dump,
    temp_file,
    _check_call,
    get_juju_major_version,
)


class BaseEnvironment(object):

    log = logging.getLogger("deployer.env")

    def __init__(self):
        self.juju_version = get_juju_major_version()

    def _check_call(self, *args, **kwargs):
        if self.options and self.options.retry_count:
            kwargs['max_retry'] = self.options.retry_count
        return _check_call(*args, **kwargs)

    def _named_env(self, params):
        if self.juju_version == 1:
            flag = "-e"
        else:
            flag = "-m"
        if self.name:
            params.extend([flag, self.name])
        return params

    def _write_config(self, svc_name, config, fh):
        fh.write(yaml_dump({svc_name: config}))
        fh.flush()

    def _get_agent_state(self, entity):
        try:
            return entity['agent-state']
        except KeyError:
            # 'agent-state' has been removed for new versions of Juju. Respond
            # with the closest status parameter.
            return entity['agent-status']['status']

    def _get_units_in_error(self, status=None):
        units = []
        if status is None:
            status = self.status()
        for s in status.get('services', {}).keys():
            for uid, u in (status['services'][s].get('units') or {}).items():
                if 'error' in self._get_agent_state(u):
                    units.append(uid)
                for uid, u in (u.get('subordinates') or {}).items():
                    if 'error' in self._get_agent_state(u):
                        units.append(uid)
        return units

    def bootstrap(self, constraints=None):
        self.log.info("bootstrapping, this might take a while...")
        params = ["juju", "bootstrap"]
        if constraints:
            params.extend(['--constraints', constraints])
        self._named_env(params)
        self._check_call(
            params, self.log, "Failed to bootstrap")
        # block until topology is returned
        self.get_cli_status()
        self.log.info(" Bootstrap complete")

    def deploy(self, name, charm_url, repo=None, config=None, constraints=None,
               resources=None, storage=None, num_units=1, force_machine=None,
               series=None, bindings=None):
        params = self._named_env(["juju", "deploy"])
        with temp_file() as fh:
            if config:
                fh.write(yaml_dump({name: config}).encode())
                fh.flush()
                params.extend(["--config", fh.name])
            if constraints:
                if isinstance(constraints, list):
                    constraints = ' '.join(constraints)
                if isinstance(constraints, dict):
                    constraints = ' '.join([
                        '{}={}'.format(k, v) for k, v in constraints.items()
                    ])
                params.extend(['--constraints', constraints])
            if resources:
                if not isinstance(resources, dict):
                    raise DeploymentError(
                        "resources must be specified as a dictionary")
                for key, value in resources.items():
                    params.append("--resource")
                    params.append("{}={}".format(key, value))
            if storage:
                if not isinstance(storage, dict):
                    raise DeploymentError(
                        "storage must be specified as a dictionary")
                params.append("--storage")
                for key, value in storage.items():
                    params.append("{}={}".format(key, value))
            if num_units not in (1, None):
                params.extend(["--num-units", str(num_units)])
            if charm_url.startswith('local'):
                if repo == "":
                    repo = "."
                params.extend(["--repository=%s" % repo])
            if force_machine is not None:
                params.extend(["--to=%s" % force_machine])
            if series and get_juju_major_version() > 1:
                params.extend(['--series', series])
            if bindings:
                if not isinstance(bindings, dict):
                    raise DeploymentError(
                        "bindings must be specified as a dictionary")
                bindings_list = []
                for key, value in bindings.items():
                    if key == "":
                        bindings_list.append("{}".format(value))
                    else:
                        bindings_list.append("{}={}".format(key, value))
                params.extend(["--bind", "%s" % " ".join(bindings_list)])

            params.extend([charm_url, name])
            self._check_call(
                params, self.log, "Error deploying application %r", name)

    def expose(self, name):
        params = self._named_env(["juju", "expose", name])
        self._check_call(
            params, self.log, "Error exposing application %r", name)

    def terminate_machine(self, mid, wait=False, force=False):
        """Terminate a machine.

        Unless ``force=True``, the machine can't have any running units.
        After removing the units or destroying the application, use
        wait_for_units to know when its safe to delete the machine (i.e.,
        units have finished executing stop hooks and are removed).

        """
        if (self.juju_version == 1 and
            ((isinstance(mid, int) and mid == 0) or
             (mid.isdigit() and int(mid) == 0))):
            # Don't kill state server
            raise RuntimeError("Can't terminate machine 0")
        if get_juju_major_version() == 1:
            terminate_action = "terminate-machine"
        else:
            terminate_action = "remove-machine"
        params = self._named_env(["juju", terminate_action])
        params.append(mid)
        if force:
            params.append('--force')
        try:
            self._check_call(
                params, self.log, "Error terminating machine %r" % mid)
        except ErrorExit as e:
            if ("machine %s does not exist" % mid) in e.error.output:
                return
            raise

    def get_service_address(self, svc_name):
        status = self.get_cli_status()
        if svc_name not in status['services']:
            self.log.warning("Application %s does not exist", svc_name)
            return None
        svc = status['services'][svc_name]
        if 'subordinate-to' in svc:
            ps = svc['subordinate-to'][0]
            self.log.info(
                'Application %s is a subordinate to %s, '
                'finding principle application'
                % (svc_name, ps))
            return self.get_service_address(svc['subordinate-to'][0])

        units = svc.get('units') or {}
        unit_keys = list(sorted(units.keys()))
        if unit_keys:
            return units[unit_keys[0]].get('public-address', '')
        self.log.warning("Application %s has no units" % svc_name)

    def get_cli_status(self):
        params = self._named_env(["juju", "status", "--format=yaml"])
        with open('/dev/null', 'w') as fh:
            output = self._check_call(
                params, self.log, "Error getting status, is it bootstrapped?",
                stderr=fh)
        status = yaml_load(output)
        return NormalizedStatus(status)

    def add_unit(self, service_name, machine_spec):
        raise NotImplementedError()

    def set_annotation(self, entity, annotations, entity_type='service'):
        raise NotImplementedError()


class NormalizedStatus(AlternateKeyDict):
    alternates = {
        'services': ('Services', 'applications'),
        'machines': ('Machines',),
        'units': ('Units',),
        'relations': ('Relations',),
        'subordinates': ('Subordinates',),
        'agent-state': ('AgentState',),
    }
