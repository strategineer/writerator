# Copyright 2012 Bill Tyros
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys
import datetime
import shelve

from contextlib import closing

import ntpath
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
             exist as well
        """
        (name, extension) = ntpath.basename(filename).split(".")
        
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