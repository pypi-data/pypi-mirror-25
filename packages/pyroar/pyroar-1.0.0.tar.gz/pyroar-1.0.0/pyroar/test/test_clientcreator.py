import unittest
from pyroar.clientfactory import ClientFactory
from pyroar.configclient import ConfigClient


class ClientCreatorTest(unittest.TestCase):
    """Tests the ConfigClient class"""
    def test_get_pokemon_client(self):
        cc = ConfigClient()
        pc = ClientFactory().get_client("pokemon", cc)

        methods = ['get', 'get_abilities', 'get_base_experience', 'get_forms',
                   'get_game_indices', 'get_height', 'get_held_items', 'get_id',
                   'get_is_default', 'get_location_area_encounters',
                   'get_methods', 'get_moves', 'get_name', 'get_order',
                   'get_species', 'get_sprites', 'get_stats', 'get_types',
                   'get_weight']
        assert pc.get_methods() == methods

        assert pc.get_weight('1') == 69
        assert pc.get_height('1') == 7

        assert pc.get_weight('charmander') == 85
        assert pc.get_height('charmander') == 6


if __name__ == '__main__':
    unittest.main()
