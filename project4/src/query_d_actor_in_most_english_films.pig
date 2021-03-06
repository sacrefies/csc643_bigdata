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


-- This Pig script is for the 4th query:
--    Which actor has appeared in the most English-language movies?
--
-- This script takes 2 command line arguments, 'inputDir' and 'outputDir'
--    which are the HDFS paths to the directory where the data files reside.
-- I.E.:
--     $ pig -param inputDir=/p4/data -param outputDir=/p4/out -f mypig.pig -x mapreduce
-- Or use a parameter file:
--     $ pig -param_file ./parameters -f mypig.pig -x mapreduce
-- Please note that -param_file must be put before -f.
--
-- Data files involved:
--    film_actor, actor, film, language

film = LOAD '$inputDir/film.csv'
       USING org.apache.pig.piggybank.storage.CSVExcelStorage(
           ',', 'NO_MULTILINE',
            'WINDOWS', 'SKIP_INPUT_HEADER')
       AS (film_id: int,
           title: chararray,
           description: chararray,
           release_year: int,
           language: int,
           rental_duration: int,
           rental_rate: double,
           length: int,
           relacement_cost: double,
           rating: chararray,
           special_features: chararray);

film_actor = LOAD '$inputDir/film_actor.csv'
       USING org.apache.pig.piggybank.storage.CSVExcelStorage(
           ',', 'NO_MULTILINE',
            'WINDOWS', 'SKIP_INPUT_HEADER')
       AS (actor_id: int,
		   film_id: int);

actor = LOAD '$inputDir/actor.csv'
       USING org.apache.pig.piggybank.storage.CSVExcelStorage(
           ',', 'NO_MULTILINE',
            'WINDOWS', 'SKIP_INPUT_HEADER')
       AS (actor_id: int,
           first_name: chararray,
           last_name: chararray);

language = LOAD '$inputDir/language.csv'
       USING org.apache.pig.piggybank.storage.CSVExcelStorage(
           ',', 'NO_MULTILINE',
            'WINDOWS', 'SKIP_INPUT_HEADER')
       AS (language_id: int,
           name: chararray);

english = FILTER language BY name MATCHES '^English$';
english_films = JOIN film BY language, english by language_id USING 'replicated';
english_film_actors = JOIN film_actor BY film_id, english_films by film::film_id USING 'replicated';
actor_films_counts = FOREACH (GROUP english_film_actors BY film_actor::actor_id)
                     GENERATE group AS actor_id,
                              COUNT(english_film_actors) AS actor_count;
actor_max_film_count = LIMIT (ORDER actor_films_counts BY actor_count DESC) 1;
which_actor = JOIN actor_max_film_count BY actor_id, actor BY actor_id USING 'replicated';
result = FOREACH which_actor
         GENERATE actor::actor_id AS actor_id,
                  actor::first_name AS first_name,
                  actor::last_name AS last_name;

STORE result INTO '$outputDir/query_d_result'
USING org.apache.pig.piggybank.storage.CSVExcelStorage(
    ',', 'NO_MULTILINE', 'UNIX', 'WRITE_OUTPUT_HEADER');
