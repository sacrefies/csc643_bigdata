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
# Copyright 2017 Jason Qiao Meng, Sarah Cooney, Mingyuan Li

# Description of this module
__doc__ = """queries.py holds multiple queries to MongoDB
which has the data imported from zipcodes.json.
The queries are from the project requirements:
    a)    Find the total number of cities in the database.
    b)    Create the list of states, cities, and city populations.
    c)    List the cities in the state of Massachusetts with populations between 1000 and 2000.
    d)    Write a mapReducer to compute the total number of cities and total population in each state.
    e)    Write a mapReducer to find the average city population for each state.
    f)    Write a mapReducer to find the least densely-populated state(s).
Each query is represented by a function.
"""

from mongodb_connector import MongoDB
from bson.code import Code






# runner
if __name__ == '__main__':
    # run the queries one by one
    print ':::::::: BigData Course Project 1: Queries to MongoDB ::::::::'
    # insert query function invocations here
    print ':::::::: Project 1 Run Ends ::::::::'
