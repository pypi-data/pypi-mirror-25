from pyroar.clientfactory import ClientFactory
import pyroar.configclient as config
from pyroar.commons import get_response


class PokeClient(object):
    """Initializes the CellBase client and allows the creation of the
     different query clients"""
    def __init__(self, config_client=None):
        # Client storage; If a client is already created, then it is returned
        self._clients = {}

        # Setting up config params
        if config_client is not None:
            try:
                assert isinstance(config_client, config.ConfigClient)
            except:
                msg = ('PokeClient configuration not properly set.' +
                       ' "pyroar.config.ConfigClient" object is needed as' +
                       ' parameter')
                raise IOError(msg)
            self._configuration = config_client
        else:
            self._configuration = config.ConfigClient()

        # Adding a new method for this class for each REST resource
        for resource in self._get_resources():
            self._add_method(resource)

    def get_methods(self):
        """Retrieves the methods of the class"""
        ms = [method for method in dir(self) if callable(getattr(self,
                                                                 method))]
        return [m for m in ms if not m.startswith('_')]

    def get_config(self):
        """Returns current configuration parameters"""
        conf = self._configuration.__dict__.items()
        conf_formatted = {}
        for k, v in conf:
            conf_formatted[k.replace('_', '')] = v
        return conf_formatted

    def get(self, resource, query_id):
        """Creates the URL for querying the REST service"""
        response = get_response(host=self._configuration.host,
                                version=self._configuration.version,
                                resource=resource,
                                query_id=query_id)

        return response.json()

    def _get_resources(self):
        """Retrieves the REST resources that can be retrieved"""
        response_json = self.get(resource=None, query_id=None)
        return map(str, response_json.keys())

    def _add_method(self, resource):
        """Adds a new method to this class"""
        client_name = resource.replace("-", "_")

        def inner_method():
            if client_name not in self._clients:
                clc = ClientFactory()
                self._clients[client_name] = clc.get_client(resource,
                                                            self._configuration)
            return self._clients[client_name]
        inner_method.__doc__ = "docstring for get_%s" % client_name
        inner_method.__name__ = "get_%s" % client_name
        setattr(self, inner_method.__name__, inner_method)
