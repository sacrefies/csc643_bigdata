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


-- load film
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
DUMP staff;
