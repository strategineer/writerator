#!/usr/bin/env python3

import logging
import sys
import datetime
import shelve
from contextlib import closing
import os
import tempfile

class DataStore(object):
    """Represents a persistent data storage framework."""

    def __init__(self, filename, key_value_pairs=[]):
        """Initializes a DataStore."""
        assert filename
        self.filename = filename
        self.db = DataStore._load_computed_data(filename, key_value_pairs)

    @staticmethod
    def _load_computed_data(source_filename, key_value_tuples=[]):
        """Loads the data into the database."""
        def set_file_last_modified_time(database, source_filename):
            """Sets filename's last modified within the db"""
            t_now = os.path.getmtime(source_filename)
            file_time_modified = datetime.datetime.fromtimestamp(t_now)
            database['file_time_modified'] = file_time_modified

        with closing(shelve.open(DataStore._get_data_source_filename(source_filename))) as database:
            for (key, value) in key_value_tuples:
                database[key] = value
            set_file_last_modified_time(database, source_filename)

        return database

    @staticmethod
    def _get_data_source_filename(source_filename):
        """
            Returns the db's filename

            SIDE EFFECT: builds directories for the files if they don't
             exist.
        """
        name = os.path.abspath(source_filename).replace(os.sep, "_")
        return tempfile.gettempdir() + os.sep + "poetcache" + name

    def __getitem__(self, key):
        """Get value associated to a key in the database"""
        with closing(shelve.open(DataStore._get_data_source_filename(self.filename))) as self.db:
            assert key in self.db.keys(), f"Key '{key}' not contained within txt database"
            value = self.db[key]
            return value

    @staticmethod
    def is_to_be_computed(source_filename):
        """Checks if Datastore's db should be recomputed."""
        data_filepath = DataStore._get_data_source_filename(source_filename)
        if not os.path.isfile(data_filepath):
            return True
        else:
            with closing(shelve.open(data_filepath)) as database:
                input_file_time = os.path.getmtime(source_filename)

                file_date_modified = datetime.datetime.fromtimestamp(input_file_time)
                data_date_modified = database["file_time_modified"]

                return str(data_date_modified) != str(file_date_modified)

def main():
    pass

if __name__== "__main__":
    main()
