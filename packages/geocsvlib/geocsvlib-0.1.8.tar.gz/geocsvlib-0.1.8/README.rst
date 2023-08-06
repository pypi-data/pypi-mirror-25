GeoCSV
------

.. image:: https://travis-ci.org/rayattack/geocsvlib.svg?branch=dev
    :target: https://travis-ci.org/rayattack/geocsvlib


GeoCSVLIB Provides utility methods for Geolocation CSV reading and parsing. A fun exercise
would be porting this to NodeJS ala NPM to take advantage of the IO asynchronicity
of Node


Installation
++++++++++++

.. code:: shell

    pip install pandas
    
    pip install geocsvlib



Parsing Geolocation CSV Data
++++++++++++++++++++++++++++

.. code:: shell

    geocsvlib data_dump.csv


Accessing Geolocation Data
++++++++++++++++++++++++++

.. code:: python
    
    from geocsvlib.models import Model
    
    ip_address = '192.168.0.1'
    
    # status is a boolean, data is hashmap or dictionary
    status, data = Model.find(ip=ip_address)

- The GeoCSV Library allows for database configuration via proision of a config.json file.

- In such scenarios you need to pass the location of the config.json file as the second argument in the terminal, or as a dictionary when loading geocsv via code.
