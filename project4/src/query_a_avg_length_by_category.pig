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
