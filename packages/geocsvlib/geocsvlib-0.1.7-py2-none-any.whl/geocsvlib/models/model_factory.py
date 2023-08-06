"""Model Factory Python Module

Model factory module returns Model DAOs that correspond
to the options provided in the config file


Module Poem
-----------

I went down to the river,
I set down on the bank.
I tried to think but couldn't,
So I jumped in and sank.

- Langston Hughes (Life is fine)
"""
from geocsvlib import get_configuration_value
from geocsvlib.constants import MONGODB, SQLITE, POSTGRES

from geocsvlib.dao.mongodb import Geolocation as IPGeolocationDocument
from geocsvlib.dao.sqlite import IPGeolocation as IPGeolocationRecord


class ModelFactory(object):
    """
    ModelFactory returns an appropriate model to use for persistence
    depending on the value provided in the library's config.json
    file
    """
    @staticmethod
    def find(**kwargs):
        """
        Virtual model abstraction that encapsulates the different db backends
        to provide a single interface to load data from the library
        """
        try:
            vendor = get_configuration_value("vendor")
        except KeyError:
            print("You need to use load geocsvlib with a configurator before use")
            return False, {}

        if vendor == MONGODB:
            return IPGeolocationDocument.finder(**kwargs)
        if vendor == SQLITE:
            # return IPGeolocationRecord
            raise NotImplementedError("sqlite support pending")
        if vendor == POSTGRES:
            # NOT YET IMPLEMENTED PROBABLY A GREAT IDEA TO RAISE AN EXC
            raise NotImplementedError("postgres support pending")

    @staticmethod
    def get_model():
        """
        Returns appropriate model to use for persistence
        """
        vendor = get_configuration_value("vendor")
        if vendor == MONGODB:
            return IPGeolocationDocument
        if vendor == SQLITE:
            # return IPGeolocationRecord
            raise NotImplementedError("sqlite support pending")
        if vendor == POSTGRES:
            # NOT YET IMPLEMENTED PROBABLY A GREAT IDEA TO RAISE AN EXC
            raise NotImplementedError("postgres support pending")
