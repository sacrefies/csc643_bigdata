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
		  
language = film = LOAD '$inputDir/language.csv'
       USING org.apache.pig.piggybank.storage.CSVExcelStorage(
           ',', 'NO_MULTILINE',
            'WINDOWS', 'SKIP_INPUT_HEADER')
       AS (language_id: int,
           name: chararray);
		   
table1 = JOIN film_actor BY film_id, film BY film_id; 
table2 = JOIN table1 BY film::language_id, language BY language_id; 

table3 = FOREACH table2 GENERATE
	table1::film_actor::actor_id AS actor_id,
	table1::film_actor::film_id AS film_id,
	table2::film::language_id AS language_id,
	table2::language::name AS language_name;

table4 = FILTER table3 BY (language_name matches 'English');

table5 = FOREACH table4 GENERATE 
	group as actor_id,
	COUNT(actor_id) AS actor_count;

table6 = ORDER table5 BY actor_count DESC; 

table7 = LIMIT table6 1; 

result = JOIN table7 BY actor_id, actor BY actor_id;

STORE result INTO '$outputDir/query_d_result'
USING org.apache.pig.piggybank.storage.CSVExcelStorage(
    ',', 'NO_MULTILINE', 'UNIX', 'WRITE_OUTPUT_HEADER');


