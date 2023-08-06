"""
If a constant name changes or is removed; Go to war
"""
from unittest import TestCase

# These are not in a test but will still cause a failure if unimportable
from geocsvlib.constants import MONGODB, POSTGRES, SQLITE


class ConstantsTest(TestCase):
    """Constants TestCase class

    Trivial class at the moment and as such no setups or teardowns necessary
    """
    def test_flag_imports(self):
        """Test constants are importable
        A simple import is enough to test the presence of wanted constants
        """
        from geocsvlib.constants import CONFIG_DEFAULT, CONFIG_FLAG, CONFIG_FLAG_HELP
        from geocsvlib.constants import CSV_HELP, DESCRIPTION

    def test_constant_values(self):
        self.assertEqual(MONGODB, 'mongodb')
        self.assertEqual(SQLITE, 'sqlite')
        self.assertEqual(POSTGRES, 'postgres')
