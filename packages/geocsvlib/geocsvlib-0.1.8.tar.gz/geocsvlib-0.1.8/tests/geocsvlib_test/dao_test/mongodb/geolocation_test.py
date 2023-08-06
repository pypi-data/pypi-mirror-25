from unittest import TestCase

import pytest

from tests import initialize_separate_test_db
from geocsvlib.dao.mongodb import GeolocationDocument as Geolocation


@pytest.mark.usefixtures('initialize_separate_test_db')
class GeolocationTest(TestCase):
    """
    """
    def setUp(self):
        self.ip_address = "192.168.0.5"
        candidate = Geolocation(
            ip_address = "192.168.0.5",
            city = "Nirvana",
            country = "Utopia",
            country_code = "UT",
            longitude = "9.78233124",
            latitude = "7.333401312",
            mystery_value = "128193721831"
        )
        candidate.save();

    def tearDown(self):
        Geolocation.objects(ip_address=self.ip_address).first().delete()

    def test_find(self):
        """
        Test that the find collection method returns a db object
        a little expensive as it saves to db and check db for saved object
        """
        is_valid, valid_result = Geolocation.find(ip_address="192.168.0.5")
        is_invalid, invalid_result = Geolocation.find(ip_address="192.168.0.10")

        self.assertTrue(is_valid)
        self.assertIsNotNone(valid_result)

        self.assertFalse(is_invalid)
        self.assertEqual(invalid_result, {})
