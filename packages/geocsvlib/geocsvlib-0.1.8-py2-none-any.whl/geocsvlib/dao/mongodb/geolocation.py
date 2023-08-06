"""IPGeolocation Data Access Object

MongoDB variant of the DAO for bidirectional (ingress and egress)
flow of data.

Module Poem
-----------

The free bird leaps
on the back of the wind
and floats downstream
till the current ends
and dips his wings
in the orange sun rays
and dares to claim the sky

- Maya Angelou
"""
from mongoengine import Document
from mongoengine import FloatField
from mongoengine import IntField
from mongoengine import StringField



class Geolocation(Document):
    """GeoCSV
    Document"""
    ip_address = StringField(required=True, unique=True)
    city = StringField(required=True)
    country = StringField(required=True)
    country_code = StringField(required=True)
    longitude = FloatField(required=True)
    latitude = FloatField(required=True)
    mystery_value = IntField(required=True)

    @staticmethod
    def find(**kwargs):
        try:
            result = Geolocation.objects(**kwargs).first()
        except:
            # log this exception
            return False, {}
        return (True, result) if result else (False, {})
