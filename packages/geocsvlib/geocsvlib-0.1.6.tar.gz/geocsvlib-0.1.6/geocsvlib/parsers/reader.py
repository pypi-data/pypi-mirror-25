"""Reader Python Module

Parses CSV file and persists

Module Poem
-----------
I am not yours, not lost in you,
Not lost, although I long to be
Lost as a candle lit at noon,
Lost as a snowflake in the sea

- Sara Teasdale (I am not yours)
"""
import csv
import numbers
import sys

from mongoengine import connect
from mongoengine import NotUniqueError
from mongoengine import ValidationError

from geocsvlib.utils import logger

from geocsvlib.models import ModelFactory
from geocsvlib.models import ConnectionFactory


class Reader(object):
    """Reader CSV Extraction Class

    parse csv file
    """
    def __init__(self, csv_filepath):
        self.csv_location = csv_filepath

        self.passed = 0
        self.failed = 0
        self.records_processed = 0
        self.total_time_taken = 0

        self.Model = ModelFactory.get_model()
        self.Connection = ConnectionFactory.get_connection()

    def _has_prerequisites(self, ip_address):
        """Minimally alidates semantic correctness of provided data"""
        subnets = ip_address.split(".")
        return len(subnets) == 4 and all(0 <= int(subnet) < 256 for subnet in subnets)

    def _is_numbery(self, value):
        """
        Validate that a value is an instance of a number
        """
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _is_processable(self, datum):
        """Parse CSV

        Parse CSV datum where datum is a list of values
        """
        if self._has_prerequisites(datum.get("ip_address")) and self._is_numbery(datum.get("mystery_value")):
            return True
        return False

    def log_csv_stats(self, outcome):
        """
        Log the statistics to be displayed at end of program run
        """
        self.records_processed += 1
        if outcome:
            self.passed += 1
        else:
            self.failed += 1

    def show_csv_stats(self, start_time, end_time):
        """
        Shows stats to stdout on the execution time and details of the CSV parsing
        """
        self.total_time_taken = end_time - start_time

        print "\n"
        print "CSV Records Processed: %r" % self.records_processed
        print "Total Time Taken (seconds): %r" % self.total_time_taken
        print "Successfully Processed and Saved: %r" % self.passed
        print "Failed to Saved: %r" % self.failed

    def process_csv_data(self):
        """Process CSV Data

        This will be much faster if we can guarantee multiprocessor environments
        """
        try:
            with open(self.csv_location, 'rb') as filestream:
                contents = csv.DictReader(filestream)
                for content in contents:
                    # always reset outcome status on new csv record
                    sys.stdout.write("\rSaving record {0} of {1}".format(contents.line_num, "Many"))
                    sys.stdout.flush()
                    status = False

                    if self._is_processable(content):
                        geocsv = self.Model(**content)
                        try:
                            status = geocsv.save()
                        except ValidationError as e:
                            msg = "Could not save GeoCSVLocation"
                            logger.message_logger(msg, e.message)
                        except NotUniqueError as e:
                            msg = "A Similar Resource Already saved On"
                            logger.message_logger(msg, e.message)
                        finally:
                            self.log_csv_stats(status)
                    else:
                        self.log_csv_stats(status)
        except IOError:
            msg = "{0} could not be opened. Check for sufficient privileges or file exists"
            print msg.format(self.csv_location)
