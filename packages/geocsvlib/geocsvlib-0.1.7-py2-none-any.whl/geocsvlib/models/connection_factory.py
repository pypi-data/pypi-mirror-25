"""
Connection Factory Python Module

Connection factory returns database connection loaders based on
the option provided in the config file

Module Poem
-----------

I stand amid the roar
Of a surf-tormented shore,
And I hold within my hand
Grains of the golden sand--
How few! yet how they creep
Through my fingers to the deep,
While I weep--while I weep!
O God! can I not grasp
Them with a tighter clasp?
O God! can I not save
One from the pitiless wave?
Is all that we see or seem
But a dream within a dream?

-Edgar Allan Poe (A Dream Within A Dream)
"""
from mongoengine import connect


class ConnectionFactory(object):
    """
    Returns appropriate connection to db
    """
    @staticmethod
    def connect(configuration):
        """
        Uses default connection or connection from options for
        code based configuration
        """
        import geocsvlib
        from geocsvlib.constants import MONGODB, SQLITE, POSTGRES
        database = configuration.get("database", "geocsvlib")
        vendor = configuration.get("vendor", "mongodb")
        port = configuration.get("port", 27017)
        host = configuration.get("url")
        config = {
            "vendor": vendor,
            "database": database,
            "port": port,
            "url": host,
            "username": "",
            "password": "",
            "csv_delimiter": ","
        }
        if vendor == MONGODB:
            geocsvlib.init(config)
            return connect(database, host=host, port=port)
        if vendor == SQLITE:
            raise NotImplementedError("sqlite support pending")
        if vendor == POSTGRES:
            raise NotImplementedError("postgres support pending")
        else:
            raise Exception("Invalid Library Configuration")

    @staticmethod
    def get_connection():
        """
        Get a connection to the provided database name and as provided
        in the configuration file and also on the config database vendor type
        """
        import geocsvlib
        from geocsvlib.constants import MONGODB, SQLITE, POSTGRES
        # use the vetted config to get the database
        vendor = geocsvlib.get_configuration_value("vendor")
        database = geocsvlib.get_configuration_value("database")
        if vendor == MONGODB:
            return connect(database)
        if vendor == SQLITE:
            raise NotImplementedError("sqlite support pending")
        if vendor == POSTGRES:
            raise NotImplementedError("postgres support pending")
        else:
            raise Exception("Invalid Library Configuration")
