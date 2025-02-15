import unittest
from posts.singletons.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def test_singleton(self):
        config1 = ConfigManager()
        config2 = ConfigManager()
        self.assertIs(config1, config2)  # Check if they are the same instance

    def test_get_set_setting(self):
        config = ConfigManager()
        self.assertEqual(config.get_setting("DEFAULT_PAGE_SIZE"), 20)
        config.set_setting("DEFAULT_PAGE_SIZE", 50)
        self.assertEqual(config.get_setting("DEFAULT_PAGE_SIZE"), 50)
        self.assertIsNone(config.get_setting("NON_EXISTENT_KEY"))

if __name__ == '__main__':
    unittest.main()