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


-- This Pig script is for the 2nd query:
--    Which categories have the longest and shortest average film lengths?
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
--    category, film_category, film


category = LOAD '$inputDir/category.csv'
           USING org.apache.pig.piggybank.storage.CSVExcelStorage(
               ',', 'NO_MULTILINE',
                'WINDOWS', 'SKIP_INPUT_HEADER')
           AS (category_id: long, name: chararray);

film_category = LOAD '$inputDir/film_category.csv'
                USING org.apache.pig.piggybank.storage.CSVExcelStorage(
                    ',', 'NO_MULTILINE',
                     'WINDOWS', 'SKIP_INPUT_HEADER')
                AS (film_id: long, category_id: long);

film = LOAD '$inputDir/film.csv'
       USING org.apache.pig.piggybank.storage.CSVExcelStorage(
           ',', 'NO_MULTILINE',
            'WINDOWS', 'SKIP_INPUT_HEADER')
       AS (film_id: long,
           title: chararray,
           description: chararray,
           release_year: long,
           language: long,
           rental_duration: long,
           rental_rate: double,
           length: long,
           relacement_cost: double,
           rating: chararray,
           special_features: chararray);
-- films with categories
categorized_films = JOIN category BY category_id, film_category BY category_id USING 'replicated';
categorized_films_full = JOIN categorized_films BY film_category::film_id, film BY film_id USING 'replicated';
-- narrow the columns
categorized_films = FOREACH categorized_films_full
                    GENERATE category::category_id AS category_id,
                             category::name AS category_name,
                             film::film_id AS film_id,
                             film::length AS film_length;
-- compute the avg
categorized = GROUP categorized_films BY (category_id, category_name);
avg = FOREACH categorized
      GENERATE FLATTEN(group),
               ROUND_TO(AVG(categorized_films.film_length), 2) AS avg_length;
-- get max/min
min_avg = LIMIT (ORDER avg BY avg_length) 1;
max_avg = LIMIT (ORDER avg BY avg_length DESC) 1;

set default_parallel 1;
result = UNION max_avg, min_avg;
--gpResult = GROUP result BY 1;
finalResult = FOREACH (GROUP result BY 1)
              GENERATE FLATTEN(result)
              AS (category_id, category_name, avg_length);

STORE finalResult INTO '$outputDir/query_b_result'
USING org.apache.pig.piggybank.storage.CSVExcelStorage(
    ',', 'NO_MULTILINE', 'UNIX', 'WRITE_OUTPUT_HEADER');
