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
from settings import COLLECTION


def total_cities(mongodb):
    """This query function returns the total number of cities in the database."""
    db = mongodb.get_database()
    return len(db[COLLECTION].distinct('city'))

def list_states_cities_populations(mongodb):
    """This query function returns the list of states, cities, populations in the database."""
    db = mongodb.get_database()
    collection = db[COLLECTION]
    array = []
    for s in collection.find():
        temp = []
        temp.append(s["state"])
        temp.append(s["city"])
        temp.append(s["pop"])
        array.append(temp)
    return array


def list_massachusetts_populations(mongodb):
    """This query function returns the list the cities in the state of Massachusetts with populations between 1000 and 2000."""
    db = mongodb.get_database()
    collection = db[COLLECTION]
    return list(collection.find({"$and": [{"state": "MA"}, {"pop": {"$gte":1000, "$lte": 2000}}]}))

def least_populated_state(mongodb):
    """A mapReducer to find the least densely-populated state(s)."""
    db = mongodb.get_database()
    collection = db[COLLECTION]
    mapper = Code("""
	             function() { emit(this.state, this.pop); };
             """)
    reducer = Code("""
	              function(state, pop) { return Array.sum(pop); };
				""")
    result = collection.map_reduce(mapper, reducer, "theResult")
    rs = result.find().sort('value', 1).limit(1)
    return {rs[0]['_id']:rs[0]['value']}


def average_state_population_with_map_reduce(mongodb):
    """A mapReducer to compute the average population in each state."""
    db = mongodb.get_database()
    collection = db[COLLECTION]
    mapper = Code('function() {for(var i = 0; i < this._id.length; i++) { var key = this.state; var value = { count: 1, pop: this.pop}; emit(key, value);} }')
    reducer = Code('function(key, values) {reduceval = {count: 0, pop: 0}; for(var i=0; i < values.length; i++) {reduceval.count += values[i].count; reduceval.pop += values[i].pop; } return reduceval; }')
    finalizer = Code('function(key, reduceval) { reduceval.avg = reduceval.pop / reduceval.count; return reduceval;}')
    result = collection.map_reduce(mapper, reducer, 'state_avgs', finalize=finalizer)
    return result.find()

def state_pop_city_count_map_reduce(mongodb):
    """A mapReducer to compute the total number of cities and total population in each state."""
    db = mongodb.get_database()
    collection = db[COLLECTION]
    mapper = Code("""
        function() {
            emit(this.state, {city: [this.city], pop: this.pop});
        };""")
    reducer = Code("""
        function(key, values) {
            var res = {city: [], pop: 0};
            for (var i = 0; i < values.length; ++i) {
                var val = values[i];
                res.pop += val.pop;
                res.city = res.city.concat(val.city);
            }
            // remove duplicates
            res.city = res.city.filter((elem, index) =>  res.city.indexOf(elem) === index);
            return res;
        }""")
    finalizer = Code("""
        function(key, reducedValue) {
            reducedValue.cityCount = reducedValue.city.length;
            return reducedValue;
        }""")
    result = collection.map_reduce(mapper, reducer, 'state_counts', finalize=finalizer)
    return result.find()

# runner
if __name__ == '__main__':
    # run the queries one by one
    print ':::::::: BigData Course Project 1: Queries to MongoDB ::::::::\n'
    mongodb = MongoDB()
    # insert query function invocations here
    print "a) Total Cities:", total_cities(mongodb), "\n"

    #print "b) States_Cities_Popuplations:", list_states_cities_populations(mongodb)

    #print "c) list_massachusetts_populations", list_massachusetts_populations(mongodb)

    print 'd) City Count and Total Population per State by Map/Reduce:'
    for r in state_pop_city_count_map_reduce(mongodb):
	    print r['_id'], ': (city count: ', r['value']['cityCount'], ', population: ', r['value']['pop'], ')'
    print "\n"

    print 'e) Average Population for Each State with MapReduce:'
    for r in average_state_population_with_map_reduce(mongodb):
	    print r['_id'], ':', r['value']['avg']
    print "\n"

    print "f) Least Populus State by Map/Reduce:",
    for (k, v) in least_populated_state(mongodb).items():
        print k, ':', v
    print "\n"

    mongodb.close()
    print ':::::::: Project 1 Run Ends ::::::::'
