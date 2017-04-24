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


-- This Pig script is for the 1st query:
--    What is the average length of films in each category?
--    List the results in alphabetic order of categories.
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
           USING org.apache.pig.piggybank.storage.CSVExcelStorage(',')
           AS (category_id: int, name: chararray);

film_category = LOAD '$inputDir/film_category.csv'
                USING org.apache.pig.piggybank.storage.CSVExcelStorage(',')
                AS (film_id: int, category_id: int);

film = LOAD '$inputDir/film.csv'
       USING org.apache.pig.piggybank.storage.CSVExcelStorage(',')
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
connect1 = JOIN category BY category_id, film_category BY category_id;
connect2 = JOIN connect1 BY film_category::film_id, film BY film_id;
x = foreach connect2 generate
    connect1::category::category_id as category_id,
    connect1::category::name as category_name,
    connect1::film_category::film_id as film_id,
    film::length as film_length;
gp = group x by (category_id, category_name);
avg = foreach gp generate FLATTEN(group), AVG(x.film_length);
DUMP avg;
