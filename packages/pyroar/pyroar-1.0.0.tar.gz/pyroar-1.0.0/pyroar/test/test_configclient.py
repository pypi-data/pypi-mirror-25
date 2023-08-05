import unittest
from pyroar.pokeclient import PokeClient
from pyroar.configclient import ConfigClient


class ConfigClientTest(unittest.TestCase):
    """Tests the ConfigClient class"""
    def test_init_config(self):
        """Checks retrieval of configuration params from config files"""
        # Default parameters
        cc = ConfigClient()
        assert cc.host == 'pokeapi.co'
        assert cc.version == 'v2'

        # Retrieving config params from YAML config file
        cc = ConfigClient('../resources/config.yml')
        assert cc.host == 'pokeapi.co'
        assert cc.version == 'v2'

        # Retrieving config params from JSON config file
        cc = ConfigClient('../resources/config.json')
        assert cc.host == 'pokeapi.co'
        assert cc.version == 'v2'

    def test_change_config(self):
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


if __name__ == '__main__':
    unittest.main()
