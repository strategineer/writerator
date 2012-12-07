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
from functools import *
import datetime
import shelve

from contextlib import closing

import os

class DataStore(object):
    """Represents a persistent data storage framework."""
    
    def __init__(self, filename):
        """Initializes a DataStore."""
        assert filename
        self.filename = filename

    def load_computed_data(self, key_value_tuples=[]):
        if not key_value_tuples:
            with closing(shelve.open(self.__get_data_filename())) as self.db:
                pass
        
        else:
            with closing(shelve.open(self.__get_data_filename())) as self.db:
                for (key, value) in key_value_tuples:
                    self.db[key] = value
    
    def set_file_last_modified_time(self):
        """Sets filename's last modified within the db"""
        with closing(shelve.open(self.__get_data_filename())) as self.db:
            t_now = os.path.getmtime(self.filename)
            file_time_modified = datetime.datetime.fromtimestamp(t_now)
            
            self.db['file_time_modified'] = file_time_modified

    def __get_data_filename(self):
        """
            Returns the db's filename without the .dat
            
            SIDE EFFECT: builds directories for the files if they don't
             exist as well
        """
        (name, extension) = self.filename.split(".")
        
        directory = "data" + os.sep + name
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        data_filename = directory + os.sep + name
        return data_filename
        
    def get_data_from_db(self, key):
        """Get value associated to a key in the database"""
        with closing(shelve.open(self.__get_data_filename())) as self.db:
            if key in self.db.keys():
                value = self.db[key]
                
                return value
        
            else:
                logging.error("Key not contained within txt database: " + key )
                sys.exit(0)
    
    def is_to_be_computed(self):
        """Checks if Datastore's db should be recomputed."""
        if not os.path.isfile(self.__get_data_filename() + ".dat"):
            return True
        
        
        else:
            with closing(shelve.open(self.__get_data_filename())) as self.db:
                input_file_time = os.path.getmtime(self.filename)
                
                file_date_modified = datetime.datetime.fromtimestamp(input_file_time)
                data_date_modified = self.db["file_time_modified"]
                
                return str(data_date_modified) != str(file_date_modified)

def main():
    pass


if __name__== "__main__":
    main()