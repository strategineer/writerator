#!/usr/bin/env python3

import logging
import sys
import datetime
import shelve
from contextlib import closing
import os

class DataStore(object):
    """Represents a persistent data storage framework."""

    def __init__(self, filename, key_value_pairs=[]):
        """Initializes a DataStore."""
        assert filename
        self.filename = filename
        self.db = DataStore._load_computed_data(filename, key_value_pairs)

    @staticmethod
    def _load_computed_data(filename, key_value_tuples=[]):
        """Loads the data into the database."""
        def set_file_last_modified_time(database, filename):
            """Sets filename's last modified within the db"""
            t_now = os.path.getmtime(filename)
            file_time_modified = datetime.datetime.fromtimestamp(t_now)
            database['file_time_modified'] = file_time_modified

        with closing(shelve.open(DataStore.__get_data_filename(filename))) as database:
            for (key, value) in key_value_tuples:
                database[key] = value
            set_file_last_modified_time(database, filename)

        return database

    @staticmethod
    def __get_data_filename(filename):
        """
            Returns the db's filename without the .dat

            SIDE EFFECT: builds directories for the files if they don't
             exist.
        """
        (name, extension) = os.path.basename(filename).split(".")
        directory = "data" + os.sep + name
        if not os.path.exists(directory):
            os.makedirs(directory)
        data_filename = directory + os.sep + name
        return data_filename

    def __getitem__(self, key):
        """Get value associated to a key in the database"""
        with closing(shelve.open(DataStore.__get_data_filename(self.filename))) as self.db:
            if key in self.db.keys():
                value = self.db[key]
                return value
            else:
                logging.error("Key not contained within txt database: " + key )
                sys.exit(1)

    @staticmethod
    def is_to_be_computed(filename):
        """Checks if Datastore's db should be recomputed."""
        if not os.path.isfile(DataStore.__get_data_filename(filename) + ".dat"):
            return True


        else:
            with closing(shelve.open(DataStore.__get_data_filename(filename))) as database:
                input_file_time = os.path.getmtime(filename)

                file_date_modified = datetime.datetime.fromtimestamp(input_file_time)
                data_date_modified = database["file_time_modified"]

                return str(data_date_modified) != str(file_date_modified)

def main():
    pass

if __name__== "__main__":
    main()
