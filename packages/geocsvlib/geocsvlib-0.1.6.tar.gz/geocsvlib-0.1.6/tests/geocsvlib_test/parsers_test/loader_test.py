from unittest import TestCase

from geocsvlib.constants import CONFIG_DEFAULT
from geocsvlib.parsers import loader

class LoaderTest(TestCase):
    """Load Configuration Test
    """

    def setUp(self):
        """Set up configuration
        """
        self.response = loader.parse_json_file(CONFIG_DEFAULT)
    
    def tearDown(self):
        """Teardown expensive ops
        """

    def test_json_loading(self):
        """Tests that json data loading function works as expected
        """
        self.assertIsNotNone(self.response)
        self.assertIsInstance(self.response, dict)
    
    def test_json_loading_correctly(self):
        """
        Ensure that the json loaded and retrieved is correct
        """
        #: remove to constants later
        default = {
            "vendor": "mongodb",
            "database": "geocsvlib",
            "port": 27017,
            "url": "localhost",
            "username": "optional",
            "password": "optional",
            "csv_delimiter": ","
        }
        self.assertListEqual(self.response.keys(), default.keys())
