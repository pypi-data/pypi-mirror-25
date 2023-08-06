"""
If a constant name changes or is removed; Go to war
"""
from unittest import TestCase


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
