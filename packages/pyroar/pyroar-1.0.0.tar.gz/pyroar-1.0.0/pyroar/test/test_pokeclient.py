import unittest
from pyroar.pokeclient import PokeClient
from pyroar.configclient import ConfigClient


class PokeClientTest(unittest.TestCase):
    """Tests the PokeClient class"""
    def test_init(self):
        """Checks the correct creation of the main client"""
        # Initialization
        pc = PokeClient()

        methods = ['get', 'get_ability', 'get_berry', 'get_berry_firmness',
                   'get_berry_flavor', 'get_characteristic', 'get_config',
                   'get_contest_effect', 'get_contest_type', 'get_egg_group',
                   'get_encounter_condition', 'get_encounter_condition_value',
                   'get_encounter_method', 'get_evolution_chain',
                   'get_evolution_trigger', 'get_gender', 'get_generation',
                   'get_growth_rate', 'get_item', 'get_item_attribute',
                   'get_item_category', 'get_item_fling_effect',
                   'get_item_pocket', 'get_language', 'get_location',
                   'get_location_area', 'get_machine', 'get_methods',
                   'get_move', 'get_move_ailment', 'get_move_battle_style',
                   'get_move_category', 'get_move_damage_class',
                   'get_move_learn_method', 'get_move_target', 'get_nature',
                   'get_pal_park_area', 'get_pokeathlon_stat', 'get_pokedex',
                   'get_pokemon', 'get_pokemon_color', 'get_pokemon_form',
                   'get_pokemon_habitat', 'get_pokemon_shape',
                   'get_pokemon_species', 'get_region', 'get_stat',
                   'get_super_contest_effect', 'get_type', 'get_version',
                   'get_version_group']

        assert pc.get_methods() == methods

    def test_config(self):
        """Checks configuration customization"""
        # Initialization
        cc = ConfigClient()
        pc = PokeClient(cc)

        # Checking some default config params
        assert pc.get_config()['host'] == 'pokeapi.co'
        assert pc.get_config()['version'] == 'v2'

        # Checking some setters for config params
        cc.host = 'pokeapi2.co'
        assert pc.get_config()['host'] == 'pokeapi2.co'
        cc.version = 'v3'
        assert pc.get_config()['version'] == 'v3'

    def test_get(self):
        """"Checks generic fetcher for RESTful service"""
        # Initialization
        pc = PokeClient()

        r = pc.get('pokemon', 'bulbasaur')
        assert r['name'] == 'bulbasaur'
        r = pc.get('pokemon', 'charmander')
        assert r['name'] == 'charmander'

        r = pc.get('pokemon', '4')
        assert r['name'] == 'charmander'
        r = pc.get('pokemon', '04')
        assert r['name'] == 'charmander'


        p = pc.get_pokemon()
        m = pc.get_machine()

        for i in p.get_types('1'):
            print i['type']['name']

        print m.get('1')

        print pc.get_config()


if __name__ == '__main__':
    unittest.main()
