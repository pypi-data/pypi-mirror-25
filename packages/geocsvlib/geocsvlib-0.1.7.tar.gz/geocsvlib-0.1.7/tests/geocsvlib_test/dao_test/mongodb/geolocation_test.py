from unittest import TestCase


from geocsvlib.dao.mongodb import Geolocation


class GeolocationTest(TestCase):
    """
    """
    def setUp(self):
        candidate = Geolocation(
            ip_address = "192.168.0.1",
            city = "Nirvana",
            country = "Utopia",
            country_code = "UT",
            longitude = "9.78233124",
            latitude = "7.333401312",
            mystery_value = "128193721831"
        )
        candidate.save();

    def tearDown(self):
        pass

    def test_find(self):
        """
        Test that the find collection method returns a db object
        a little expensive as it saves to db and check db for saved object
        """
        valid_result = Geolocation.find("192.168.0.5")
        invalid_result = Geolocation.find("192.168.0.1")

        self.assertIsNotNone(valid_result)
        self.assertIsNone(invalid_result)
