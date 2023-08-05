from setuptools import setup


# Getting long description
def get_long_description():
    with open('README.rst') as f:
        long_desc = f.read()
    return long_desc


setup_kwargs = {
    'name': 'pyroar',
    'version': '1.0.0',
    'description': 'Python client for PokeAPI',
    'long_description': get_long_description(),
    'author': 'Daniel Perez-Gil',
    'author_email': 'dperezgil89@gmail.com',
    'url': 'https://github.com/dapregi/pyroar',
    'packages': ['pyroar'],
    'package_dir': {'pyroar': 'pyroar'},
    'requires': ['pyyaml']
}

setup(**setup_kwargs)
