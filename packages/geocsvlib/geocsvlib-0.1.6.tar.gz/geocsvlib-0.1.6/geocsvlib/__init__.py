"""GeoCSVlib

Parses Geolocation data from CSV files for persistence and lookup

Module Poem
-----------
Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;
Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,
And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever come back.
I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I-
I took the one less traveled by,
And that has made all the difference

- Robert Frost (The Road Not Taken)
"""


_configuration = {"config": {
    "vendor": "mongodb",
    "database": "pyishdb"
}}


def init(configuration):
    """Initialize Configuration of Library"""
    _configuration["config"] = configuration


def get_configuration_value(keyword):
    """
    Returns the value of a configuration key if set
    """
    return _configuration["config"].get(keyword)
