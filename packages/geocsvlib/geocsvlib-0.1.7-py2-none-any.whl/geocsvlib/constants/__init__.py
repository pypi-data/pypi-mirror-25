"""Constants Utility Package

Holds library wide constants to provide a single point of concern/editing
for application/library constants

Module Poem
-----------

here is the deepest secret nobody knows
(here is the root of the root and the bud of the bud
and the sky of the sky of a tree called life;which grows
higher than the soul can hope or mind can hide)
and this is the wonder that's keeping the stars apart

I carry your heart(I carry it in my heart)

- EE Cummings (I Carry Your Heart With Me)
"""
CONFIG_DEFAULT = 'config.json'
CONFIG_FLAG = '--config'
CONFIG_FLAG_HELP = 'config.json file to use for database configuration'

CSV_HELP = 'Name of the CSV file to be parsed'

DESCRIPTION = 'Geolocation CSV Parser, Persistor, and Loader Library'

MONGODB = "mongodb"
SQLITE = "sqlite"
POSTGRES = "postgres"
ALLOWED_DATABASES = [MONGODB, SQLITE, POSTGRES]


__all__ = [
    'MONGODB'
]
