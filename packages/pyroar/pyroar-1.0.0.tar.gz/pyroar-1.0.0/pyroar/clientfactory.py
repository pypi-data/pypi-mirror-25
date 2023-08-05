from pyroar.commons import get_response


class RestClient(object):
    """Base client class"""
    def __init__(self, configuration, resource):
        self._configuration = configuration
        self._resource = resource

    def get(self, query_id):
        """Queries the REST service and returns the result"""
        response = get_response(host=self._configuration.host,
                                version=self._configuration.version,
                                resource=self._resource,
                                query_id=query_id)

        return response.json()

    def get_methods(self):
        """Retrieves the methods of the class"""
        ms = [method for method in dir(self) if callable(getattr(self,
                                                                 method))]
        return [m for m in ms if not m.startswith('_')]


class ClientFactory(object):
    """REST client factory"""
    def __init__(self):
        pass

    def get_client(self, resource, configuration):
        """Creates a new client for a given REST resource"""
        return self._get_custom_class(resource, configuration)

    def _get_custom_class(self, name, configuration):
        """Creates a new REST client and adds methods to it"""
        # Creating the class and instantiating it
        CustomClass = self._create_class(name)
        custom_class = CustomClass(configuration)
        # Adding custom methods to the class
        for value in custom_class.get("1").keys():
            self._add_method(CustomClass, str(value))
        return custom_class

    def _add_method(self, cls, i):
        """Adds a new method to a custom class"""
        def inner_method(self, query_id):
            return self.get(query_id)[i]
        inner_method.__doc__ = "docstring for get_%s" % i
        inner_method.__name__ = "get_%s" % i
        setattr(cls, inner_method.__name__, inner_method)

    def _create_class(self, resource, RestClient=RestClient):
        """Creates a new client class from RestClient"""
        def __init__(self, configuration):
            RestClient.__init__(self, configuration, resource)
        new_class = type(resource, (RestClient,), {"__init__": __init__})
        return new_class
