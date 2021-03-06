-- Copyright 2017 team1@course_bigdata, Saint Joseph's University
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--    http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.


-- This Pig script is for the 6th query:
--    Alphabetically list actors
--    who appeared in the movie with the largest cast of actors.
--
-- This script takes 2 command line arguments, 'inputDir' and 'outputDir'
--    which are the HDFS paths to the directory where the data files reside.
-- I.E.:
--     $ pig -param inputDir=/p4/data -param outputDir=/p4/out -f mypig.pig -x mapreduce
-- Or use a parameter file:
--     $  pig -param_file parameters -f query_f_actor_names_movie_largest_cast.pig -x mapreduce
-- Please note that -param_file must be put before -f.
--
-- Data files involved:
--    film_actor, actor


-- data loading: be aware of the EOL that in the data files: It's Windows CRLF.
film_actors = LOAD '$inputDir/film_actor.csv'
              USING org.apache.pig.piggybank.storage.CSVExcelStorage(
                  ',', 'NO_MULTILINE',
                  'WINDOWS', 'SKIP_INPUT_HEADER')
              AS (actor_id:long, film_id:long);

actors = LOAD '$inputDir/actor.csv'
         USING org.apache.pig.piggybank.storage.CSVExcelStorage(
             ',', 'NO_MULTILINE',
              'WINDOWS', 'SKIP_INPUT_HEADER')
         AS (actor_id:long, fname:chararray, lname:chararray);

-- group film_actors with actor counts
actor_counts = FOREACH (GROUP film_actors BY film_id)
               GENERATE group AS film_id:long,
                        COUNT(film_actors) AS actor_count:long;
-- sort film group by actor counts
sorted_actor_counts = ORDER actor_counts BY actor_count DESC;
-- top 1: the film which has the maximum actor count
max_actor_counts = LIMIT sorted_actor_counts 1;
-- get film ids which have the max count of actors
tmp = JOIN sorted_actor_counts BY actor_count, max_actor_counts BY actor_count USING 'replicated';
films_max_actor_counts = FOREACH tmp GENERATE sorted_actor_counts::film_id AS film_id;
-- get the actors in the films from films_max_actor_counts
tmp = JOIN film_actors BY film_id, films_max_actor_counts BY film_id USING 'replicated';
actor_ids = FOREACH tmp GENERATE film_actors::actor_id AS actor_id;
actor_ids = DISTINCT actor_ids;
-- generate actor names
tmp = JOIN actors BY actor_id, actor_ids BY actor_id USING 'replicated';
actor_names = FOREACH tmp
              GENERATE actors::actor_id as actor_id,
                       actors::fname as first_name,
                       actors::lname as last_name;
-- order the names
ordered_actors = ORDER actor_names BY last_name, first_name;

STORE ordered_actors INTO '$outputDir/query_f_result'
USING org.apache.pig.piggybank.storage.CSVExcelStorage(
    ',', 'NO_MULTILINE', 'UNIX', 'WRITE_OUTPUT_HEADER');
