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


-- This Pig script is for the 3rd query:
--    Which customers have rented action but not comedy or classic movies?
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
--    rental, customer, inventory, film, film_category, category

category = LOAD '$inputDir/category.csv'
           USING org.apache.pig.piggybank.storage.CSVExcelStorage(
               ',', 'NO_MULTILINE',
                'WINDOWS', 'SKIP_INPUT_HEADER')
           AS (category_id: int, name: chararray);

film_category = LOAD '$inputDir/film_category.csv'
                USING org.apache.pig.piggybank.storage.CSVExcelStorage(
                    ',', 'NO_MULTILINE',
                     'WINDOWS', 'SKIP_INPUT_HEADER')
                AS (film_id: int, category_id: int);

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

customer = LOAD '$inputDir/customer.csv'
         USING org.apache.pig.piggybank.storage.CSVExcelStorage(
             ',', 'NO_MULTILINE',
             'WINDOWS', 'SKIP_INPUT_HEADER')
         AS (customer_id:int,
             store_id:int,
			 first_name:chararray,
			 last_name:chararray,
			 email:chararray,
             address_id:int,
             active:int);
-- prepare the information needed
film_inventory_w_category = JOIN film BY film_id, film_category BY film_id, inventory BY film_id;
film_full_info = JOIN film_inventory_w_category BY film_category::category_id, category BY category_id;
film_inventory_rented = JOIN film_full_info BY inventory::inventory_id, rental BY inventory_id;
customers_who_rented_films = JOIN film_inventory_rented BY rental::customer_id, customer BY customer_id;
-- generate a smaller table with fields only needed
customer_film_info = FOREACH customers_who_rented_films
                     GENERATE customer::customer_id AS customer_id,
                              customer::first_name AS first_name,
                              customer::last_name AS last_name,
                              category::name AS category_name;
-- customers who have not rented 'Comedy' or 'Classics'
customers_not_rented_comedy_classic = FILTER customer_film_info BY category_name matches '^(?!(Comedy|Classics)).*$';
-- customers who have rented 'Action' out of customers_not_rented_comedy_classic
customers_rented_action = ORDER (DISTINCT (FILTER customers_not_rented_comedy_classic BY category_name matches '^(Action)$'))
                          BY last_name, first_name;

-- customers who have rented 'ACTION' but not 'Comedy' or 'Classics'
customers_info = FOREACH customers_rented_action
                 GENERATE first_name as first_name,
                          last_name as last_name;

STORE customers_info INTO '$outputDir/query_c_result'
USING org.apache.pig.piggybank.storage.CSVExcelStorage(
    ',', 'NO_MULTILINE', 'UNIX', 'WRITE_OUTPUT_HEADER');
