#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# Copyright 2017 Jason Qiao Meng

__doc__ = """This file contains the global settings for this program.
"""

# database related
DB_NAME = "zipcodes"
DB_PROTOCOL = "mongodb://"
DB_HOST = "localhost"
DB_PORT = "27017"
COLLECTION = "zipcodes"


# unit tests
from pymongo import MongoClient

if __name__ == '__main__':
    conn_string = "%s%s:%s/" % (DB_PROTOCOL, DB_HOST, DB_PORT);
    print conn_string

    # test mongoDB connection
    client = MongoClient(conn_string)
    for db in client.database_names():
        print '%s, ' % db ,
    client.close()
