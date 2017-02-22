#!/usr/bin/env python
# -*- coding: <encoding name> -*-
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

__doc__ = """mongodb_connector.py provides a conventient way to get a MongoDB
database object.
"""

from settings import DB_NAME, DB_PROTOCOL, DB_HOST, DB_PORT, COLLECTION
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidName


class MongoDB(object):
    """A class to connect to a MongoDB according to the settings.py"""

    def __init__(self):
        """Create and initialize an instance of class MongoDB"""
        self.__conn_str = None
        self.__client = None
        self.__db = None

    def simple_connction_string(self):
        """Get the connection string.

        :return: A legal MongoDB connection string from the settings.
        """
        self.__conn_str = "%s%s:%s/" % (DB_PROTOCOL, DB_HOST, DB_PORT)
        return self.__conn_str

    def get_client(self):
        """Connect to the MongoDB and return a client object.
        Refer to: http://api.mongodb.com/python/current/api/pymongo/mongo_client.html#pymongo.mongo_client.MongoClient

        :return: An instance of class MongoClient
        """
        if self.__client:
            return self.__client

        self.__client = MongoClient(self.simple_connction_string())
        try:
            # The ismaster command is cheap and does not require auth.
            self.__client.admin.command('ismaster')
        except ConnectionFailure as cf:
            print 'Connecting to MongoDB failed: ', cf
            self.__client = None

        return self.__client

    def get_database(self, name=None):
        """Get the database object with the specified name.

        :param name: The name of the database. If given None or omitted,
                     this method use the name set in the settings file.
        :return: An instance of Database.
        """
        if not self.__client:
            self.get_client()

        dbname = name if name else DB_NAME
        try:
            self.__db = self.__client[dbname]
        except InvalidName as ine:
            self.__db = None
            print 'No such database: %s. %s' % (dbname, ine)

        return self.__db

    def close(self):
        if self.__client:
            self.__client.close()
        self.__db = None
        self.__client = None
        self.__conn_str = None


# unit tests
if __name__ == '__main__':
    mongo = MongoDB()
    cli = mongo.get_client()
    if cli and cli.database_names():
        print 'connect successful'
        print 'databases: ',
        for n in cli.database_names():
            print '%s, ' % n,
        print ''
    db = mongo.get_database()
    if db:
        print 'database connected'
        print 'database test collections: ',
        for n in db.collection_names():
            print '%s, ' % n,
        print ''
        print 'database test get document count: ',
        collection = db[db.collection_names()[0]]
        print collection.count()
    mongo.close();
    print 'Test finished'
