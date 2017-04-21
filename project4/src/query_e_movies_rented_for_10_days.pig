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
--    How many distinct movies were rented for exactly 10 days
--    from the store where Mike works?
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
--    film, inventory, rental, store, staff

-- data loading: be aware of the EOL that in the data files: It's Windows CRLF.
staff = LOAD '$inputDir/staff.csv'
        USING org.apache.pig.piggybank.storage.CSVExcelStorage(
            ',', 'NO_MULTILINE',
             'WINDOWS', 'SKIP_INPUT_HEADER')
        AS (staff_id:int,
            fname:chararray,
            lname:chararray,
            address_id:int,
            email:chararray,
            store_id:int,
            active:int,
            username:chararray,
            password:chararray);

film = LOAD '$inputDir/film.csv'
       USING org.apache.pig.piggybank.storage.CSVExcelStorage(
           ',', 'NO_MULTILINE',
            'WINDOWS', 'SKIP_INPUT_HEADER')
       AS (film_id:int,
           title:chararray,
           description:chararray,
           release_year:int,
           language_id:int,
           rental_duration:int,
           rental_rate:double,
           length:int,
           replacement_cost:double,
           rating:chararray,
           special_features:chararray);

inventory = LOAD '$inputDir/inventory.csv'
            USING org.apache.pig.piggybank.storage.CSVExcelStorage(
                ',', 'NO_MULTILINE',
                'WINDOWS', 'SKIP_INPUT_HEADER')
            AS (inventory_id:int,
                film_id:int,
                store_id:int);

rental = LOAD '$inputDir/rental.csv'
         USING org.apache.pig.piggybank.storage.CSVExcelStorage(
             ',', 'NO_MULTILINE',
             'WINDOWS', 'SKIP_INPUT_HEADER')
         AS (rental_id:int,
             rental_date:chararray,
             inventory_id:int,
             customer_id:int,
             return_date:chararray,
             staff_id:int);

stores = LOAD '$inputDir/store.csv'
         USING org.apache.pig.piggybank.storage.CSVExcelStorage(
             ',', 'NO_MULTILINE',
             'WINDOWS', 'SKIP_INPUT_HEADER')
         AS (store_id:int, address_id:int);

-- get Mike
mike = FILTER staff BY (fname matches '^Mike');
-- get the rented which are more than 10 days
rented = FILTER rental
         BY DaysBetween(
             ToDate(REPLACE(return_date, '\\s+', ' '), 'yyyy-MM-dd HH:mm:ss'),
             ToDate(REPLACE(rental_date, '\\s+', ' '), 'yyyy-MM-dd HH:mm:ss')
             ) >= 5;
-- we need the inventory_ids only
rented_inventory = FOREACH rented GENERATE inventory_id as inventory_id:int;
-- get inventory by store, only inventory_id, film_id are needed:
film_inventory = FOREACH (JOIN mike BY store_id, stores BY store_id, inventory by store_id)
                 GENERATE inventory_id, film_id;
-- get film_ids whose rental duration are more than 10 days
filmIds = FOREACH (JOIN rented_inventory BY inventory_id, film_inventory BY inventory_id)
        GENERATE film_id AS film_id:int;

films = FOREACH (JOIN filmIds by film_id, film by film_id)
        GENERATE film::film_id AS film_id:int,
                 film::title AS title:chararray;
final = DISTINCT films;

STORE final INTO '$outputDir/query_e_result'
USING org.apache.pig.piggybank.storage.CSVExcelStorage(',', 'NO_MULTILINE', 'UNIX', 'WRITE_OUTPUT_HEADER');
