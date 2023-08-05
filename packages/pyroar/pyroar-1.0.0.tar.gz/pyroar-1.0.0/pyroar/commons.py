import requests


def _create_rest_url(host, version, resource, query_id):
    """Creates the URL for querying the REST service"""
    pokeapi_rest = 'api'

    # Creating the basic URL
    url_parts = [host, pokeapi_rest, version]

    # Checking for reource and query_id
    if resource is not None:
        url_parts.append(resource)
    if query_id is not None:
        url_parts.append(query_id)

    url = ('http://' + '/'.join(url_parts))
    return url


def get_response(host, version, resource=None, query_id=None):
    """Creates the URL for querying the REST service"""
    url = _create_rest_url(host, version, resource, query_id)
    response = requests.get(url, headers={"Accept-Encoding": "gzip"})

    # print(url)
    return response
