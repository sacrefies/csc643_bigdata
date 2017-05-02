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


-- This Pig script is for the 5th query:
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
--    film, inventory, rental, staff


-- data loading: be aware of the EOL that in the data files: It's Windows CRLF.
staff = LOAD '$inputDir/staff.csv'
        USING org.apache.pig.piggybank.storage.CSVExcelStorage(
            ',', 'NO_MULTILINE',
             'WINDOWS', 'SKIP_INPUT_HEADER')
        AS (staff_id:long,
            fname:chararray,
            lname:chararray,
            address_id:long,
            email:chararray,
            store_id:long,
            active:long,
            username:chararray,
            password:chararray);

film = LOAD '$inputDir/film.csv'
       USING org.apache.pig.piggybank.storage.CSVExcelStorage(
           ',', 'NO_MULTILINE',
            'WINDOWS', 'SKIP_INPUT_HEADER')
       AS (film_id:long,
           title:chararray,
           description:chararray,
           release_year:long,
           language_id:long,
           rental_duration:int,
           rental_rate:double,
           length:long,
           replacement_cost:double,
           rating:chararray,
           special_features:chararray);

inventory = LOAD '$inputDir/inventory.csv'
            USING org.apache.pig.piggybank.storage.CSVExcelStorage(
                ',', 'NO_MULTILINE',
                'WINDOWS', 'SKIP_INPUT_HEADER')
            AS (inventory_id:long,
                film_id:long,
                store_id:long);

rental = LOAD '$inputDir/rental.csv'
         USING org.apache.pig.piggybank.storage.CSVExcelStorage(
             ',', 'NO_MULTILINE',
             'WINDOWS', 'SKIP_INPUT_HEADER')
         AS (rental_id:long,
             rental_date:chararray,
             inventory_id:long,
             customer_id:long,
             return_date:chararray,
             staff_id:long);
rented_w_days = FOREACH rental
                GENERATE rental_id, inventory_id,
                          DaysBetween(
                              ToDate(REPLACE(return_date, '\\s+', ' '), 'yyyy-MM-dd HH:mm:ss', 'UTC'),
                              ToDate(REPLACE(rental_date, '\\s+', ' '), 'yyyy-MM-dd HH:mm:ss', 'UTC')
                          ) AS days:long,
                          HoursBetween(
                              ToDate(REPLACE(return_date, '\\s+', ' '), 'yyyy-MM-dd HH:mm:ss', 'UTC'),
                              ToDate(REPLACE(rental_date, '\\s+', ' '), 'yyyy-MM-dd HH:mm:ss', 'UTC')
                          ) AS hours:long;
-- get Mike's store and inventory
mike = FILTER staff BY (fname MATCHES '^Mike$');
stores_mike_inventory = JOIN inventory BY store_id, mike BY store_id;
stores_mike_inventory = FOREACH stores_mike_inventory
                        GENERATE inventory::inventory_id AS inventory_id,
                                 inventory::film_id AS film_id;
-- rented films for 10 days
rented_10d = FILTER rented_w_days BY (hours / 24.0 > 9.0) AND (days == 9);
rented_mike_store_10d = JOIN rented_10d BY inventory_id,
                             stores_mike_inventory BY inventory_id;
films_10d = FOREACH rented_mike_store_10d
            GENERATE stores_mike_inventory::film_id AS film_id;
-- get unique ids
unique_films_10d = DISTINCT films_10d;
-- get the count
final = FOREACH (GROUP unique_films_10d ALL)
        GENERATE COUNT(unique_films_10d);

STORE final INTO '$outputDir/query_e_result'
USING org.apache.pig.piggybank.storage.CSVExcelStorage(
    ',', 'NO_MULTILINE', 'UNIX', 'WRITE_OUTPUT_HEADER');
