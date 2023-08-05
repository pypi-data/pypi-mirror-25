.. contents::

PyRoar
======

- This Python package aims to provide easy acces to the data served by the `Pokéapi`_ RESTful service.

- This project was conceived as a way to learn how to create classes and methods dynamically. Therefore, RESTful client classes and methods to retrieve data are not explicitly defined. Instead, the Pokéapi service is asked for the resources it provides and classes and methods are created in real time. This allows adaptability to the service but can cause some problems if it goes through major changes.

Pokéapi - The RESTful Pokémon API
---------------------------------

- `Pokéapi`_ (Copyright Paul Hallett) is a RESTful API interface to highly detailed data related to the `Pokémon`_ video game franchise.

- Using this RESTful service you can consume information on Pokémon, their moves, abilities, types, egg groups, etc.

- For more information, please read the `Pokéapi V2 Documentation`_.


Installation
------------

Cloning
```````
PyRoar can be cloned in your local machine by executing in your terminal::

   $ git clone https://github.com/dapregi/PyRoar.git

Once you have downloaded the project you can install the library::

   $ cd pyroar
   $ python setup.py install

Usage
-----

Getting started
```````````````
The first step is to import the module and initialize the PokeClient:

.. code-block:: python

    >>> from pyroar.pokeclient import PokeClient
    >>> pc = PokeClient()

The second step is to create the specific client for the data we want to query:

.. code-block:: python

   >>> pokemon = pc.get_pokemon()
   >>> berry = pc.get_berry()
   >>> machine = pc.get_machine()

And now, you can start asking to the Pokéapi service by providing a query ID:

.. code-block:: python

    >>> pokemon.get_height('bulbasaur')
    7

    >>> pokemon.get_types('bulbasaur')
    [{u'slot': 2, u'type': {u'name': u'poison', u'url': u'http://pokeapi.co/api/v2/type/4/'}}, {u'slot': 1, u'type': {u'name': u'grass', u'url': u'http://pokeapi.co/api/v2/type/12/'}}]

    >>> berry.get_growth_time('cheri')
    3

    >>> machine.get_move('1')
    {u'name': u'mega-punch', u'url': u'http://pokeapi.co/api/v2/move/5/'}

Some data can be accessed specifying either id or name:

.. code-block:: python

    >>> pokemon.get_weight('bulbasaur')
    69
    >>> pokemon.get_weight('1')
    69

Results are retrieved as JSON formatted data. Therefore, they can be queried by key:

.. code-block:: python

    >>> for type in pokemon.get_types('bulbasaur'):
    ...     print type['type']['name']
    poison
    grass

    >>> machine.get_move('1')['name']
    mega-punch

To retrieve all the information for a resource just use the method "get()"

.. code-block:: python

    >>> pc.get('machine', '1')
    {u'item': {u'url': u'http://pokeapi.co/api/v2/item/305/', u'name': u'tm01'}, u'move': {u'url': u'http://pokeapi.co/api/v2/move/5/', u'name': u'mega-punch'}, u'id': 1, u'version_group': {u'url': u'http://pokeapi.co/api/v2/version-group/1/', u'name': u'red-blue'}}

    >>> machine.get('1')
    {u'item': {u'url': u'http://pokeapi.co/api/v2/item/305/', u'name': u'tm01'}, u'move': {u'url': u'http://pokeapi.co/api/v2/move/5/', u'name': u'mega-punch'}, u'id': 1, u'version_group': {u'url': u'http://pokeapi.co/api/v2/version-group/1/', u'name': u'red-blue'}}

What can I ask for?
```````````````````
As client classes and client methods are dynamically created, the best way to know the methods of an object is either checking out the `Pokéapi V2 Documentation`_ or using the built-in method "get_methods()":

.. code-block:: python

    >>> pc.get_methods()
    ['get', 'get_ability', 'get_berry', 'get_berry_firmness',
     'get_berry_flavor', 'get_characteristic', 'get_config',
     'get_contest_effect', 'get_contest_type', 'get_egg_group',
     'get_encounter_condition', 'get_encounter_condition_value',
     'get_encounter_method', 'get_evolution_chain', 'get_evolution_trigger',
     'get_gender', 'get_generation', 'get_growth_rate', 'get_item',
     'get_item_attribute', 'get_item_category', 'get_item_fling_effect',
     'get_item_pocket', 'get_language', 'get_location', 'get_location_area',
     'get_machine', 'get_methods', 'get_move', 'get_move_ailment',
     'get_move_battle_style', 'get_move_category', 'get_move_damage_class',
     'get_move_learn_method', 'get_move_target', 'get_nature',
     'get_pal_park_area', 'get_pokeathlon_stat', 'get_pokedex', 'get_pokemon',
     'get_pokemon_color', 'get_pokemon_form', 'get_pokemon_habitat',
     'get_pokemon_shape', 'get_pokemon_species', 'get_region', 'get_stat',
     'get_super_contest_effect', 'get_type', 'get_version', 'get_version_group']

    >>> pokemon.get_methods()
    ['get', 'get_abilities', 'get_base_experience', 'get_forms',
     'get_game_indices', 'get_height', 'get_held_items', 'get_id',
     'get_is_default', 'get_location_area_encounters', 'get_methods',
     'get_moves', 'get_name', 'get_order', 'get_species', 'get_sprites',
     'get_stats', 'get_types', 'get_weight']


Configuration
`````````````

Configuration stores the REST services host and the API version.

Default configuration:

.. code-block:: python

    >>> pc.get_config()
    {'host': 'pokeapi.co', 'version': 'v2'}

A custom configuration can be passed to PokeClient with a ConfigClient object. JSON and YML files are supported:

.. code-block:: python

    >>> cc = ConfigClient('config.json')
    >>> pc = PokeClient(cc)

If you want to change the configuration you can directly modify the ConfigClient object:

.. code-block:: python

    >>> cc = ConfigClient()
    >>> pc = PokeClient(cc)
    >>> pc.get_config()
    {'host': 'pokeapi.co', 'version': 'v2'}
    >>> cc.version = 'v3'
    >>> pc.get_config()
    {'host': 'pokeapi.co', 'version': 'v3'}

WARNING
```````
From `Pokéapi V2 Documentation`_:

- This is a **consumption-only** API - only the HTTP GET method is available on resources. No authentication is required to access this API. All resources are fully open and available.

- **No authentication** is required to access this API. All resources are fully open and available.

  - There is, however, a daily rate limit of 300 requests **per resource** per IP address. So a single IP address can call the bulbasaur resource 300 times a day. Not 300 requests across the entire dataset! This is to stop our database from falling over under heavy load.

- If you are going to be regularly using the API, I recommend caching data on your service.

  - Luckily, we provide **modified/created datetime stamps** on every single resource so you can check for updates (and thus make your caching efficient)

License
-------

PyRoar is `free software`_. Licensed mainly under the General Public License (GPL_).
For more details on the licensing take a look at the LICENSE.txt file.

Trivia
------

- This project is named after the Pokémon `Pyroar`_.


.. _Pokéapi: https://pokeapi.co/
.. _Pyroar: http://bulbapedia.bulbagarden.net/wiki/Pyroar_(Pok%C3%A9mon)
.. _Pokémon: https://en.wikipedia.org/wiki/Pok%C3%A9mon
.. _Pokéapi V2 Documentation: https://pokeapi.co/docsv2/
.. _free software: http://en.wikipedia.org/wiki/Free_software
.. _GPL: http://www.gnu.org/copyleft/gpl.html