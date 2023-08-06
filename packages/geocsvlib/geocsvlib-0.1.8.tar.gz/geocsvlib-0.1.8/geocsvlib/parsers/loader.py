"""Loader Python Module

Load provided json configuration file for database connectivity
"""
import json


def parse_json_file(json_file_url):
    """
    Parse provided json file and save as global configuration object for
    later library reuse
    """
    with open(json_file_url) as json_configuration:
        try:
            configuration = json.load(json_configuration)
            return configuration
        except AttributeError:
            print("Invalid json file detected, please try again later")
        except ValueError:
            print("Invalid data file, could not decode into json")
