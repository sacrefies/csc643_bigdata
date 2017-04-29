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
			 
table1 = JOIN customer BY customer_id, rental BY customer_id;
table2 = JOIN table1 BY table1::rental::inventory_id, inventory BY inventory_id;
table3 = JOIN table2 BY table2::inventory::film_id, film BY film_id;
table4 = JOIN table3 BY table3::film::film_id, film_category BY film_id;
table5 = JOIN table4 BY table4::film_category::category_id, category BY category_id;

table6 = FOREACH table5 GENERATE 
	table1::customer::customer_id AS customer_id,
	table1::customer::first_name AS first_name,
	table1::customer::last_name AS last_name,
	table1::rental::rental_id AS rental_id, 
	table2::inventory::inventory_id AS inventory_id,
	table3::film::film_id AS film_id,
	table4::film_category::category_id AS category_id,
	table5::category::name AS category_name;
	
table7 = FILTER table6 BY ((category_name matches 'Action') 
							AND NOT (category_name matches 'Comedy')
							AND NOT (category_name matches 'Classics'));
							
table8 = FOREACH table7 GENERATE 
		table7::customer_id AS customer_id,
		table7::first_name AS first_name,
		table7::last_name AS last_name;
		
result = GROUP table8 BY customer_id;

STORE result INTO '$outputDir/query_c_result'
USING org.apache.pig.piggybank.storage.CSVExcelStorage(
    ',', 'NO_MULTILINE', 'UNIX', 'WRITE_OUTPUT_HEADER');




