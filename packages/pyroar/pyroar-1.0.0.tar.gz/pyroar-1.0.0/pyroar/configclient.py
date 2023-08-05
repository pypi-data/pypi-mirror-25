import json
import yaml


class ConfigClient(object):
    """Sets up the default configuration for the CellBase client"""
    def __init__(self, config_fpath=None):
        # Default config params
        self._host = 'pokeapi.co'
        self._version = 'v2'

        # If config file is provided, override default config params
        if config_fpath is not None:
            self._override_config_params(config_fpath)

    def _override_config_params(self, config_fpath):
        """Overrides config params if config file is provided"""
        config_fhand = open(config_fpath, 'r')

        config_dict = None
        if config_fpath.endswith('.yml') or config_fpath.endswith('.yaml'):
            config_dict = yaml.safe_load(config_fhand)

        if config_fpath.endswith('.json'):
            config_dict = json.loads(config_fhand.read())

        if config_dict is not None:
            if 'host' in config_dict:
                self._host = config_dict['host']
            if 'version' in config_dict:
                self._version = config_dict['version']

        config_fhand.close()

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, new_version):
        self._version = new_version

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, new_host):
            self._host = new_host
