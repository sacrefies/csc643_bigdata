<!--
Copyright 2017 team1@course_bigdata, Saint Joseph's University

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->


# Project 4: Apache Pig Latin Exercise

*This project is developed by* ***Team 1***:
* Sarah Cooney
* Mingyuan Li
* Jason Qiao Meng

<div class="page-break"></div>

## Table of Content
- [Project 4: Apache Pig Latin Exercise](#project-4-apache-pig-latin-exercise)
    - [Table of Content](#table-of-content)
    - [Introduction](#introduction)
        - [Entity Relations](#entity-relations)
        - [License](#license)
    - [Implementation](#implementation)
        - [Parameter File](#parameter-file)
        - [Class CSVExcelStorage](#class-csvexcelstorage)
        - [Query A](#query-a)
        - [Query B](#query-b)
        - [Query C](#query-c)
        - [Query D](#query-d)
        - [Query E](#query-e)
        - [Query F](#query-f)
    - [Running the Pig Latin Scripts](#running-the-pig-latin-scripts)
- [About Team 1](#about-team-1)


## Introduction
This project is the final project of CSC643. It works with the [Apache Pig Latin][pig_latin] and the [Apache Hadoop][apache_hadoop]. It is about a set of `Pig Latin` scripts which are to be executed on a `Hadoop` cluster of 2.

The scripts take the `.csv` data files under `<project_root_path>/input/` as the input data, produce results for the following problems:
1. What is the average length of films in each category? List the results in alphabetic order of categories.
1. Which categories have the longest and shortest average film lengths?
1. Which customers have rented action but not comedy or classic movies?
1. Which actor has appeared in the most English-language movies?
1. How many distinct movies were rented for exactly 10 days from the store where Mike works?
1. Alphabetically list actors who appeared in the movie with the largest cast of actors.

*For team member contributions, see: [workload and responsibilities][ranking]*

### Entity Relations
The following figure shows the relations that are separately stored in the `.csv` files:
![alter text](entity_relations.jpg "Entity Relations")
*Figure 1: Entity Relations*

### License
*Apache License V2.0* is applied to this project.

## Implementation
By using the [Apache Pig Latin][pig_releases], the `Hadoop` map/reduce process can be abstracted and transformed to a script like `SQL`. In this fashion, a map/reduce process can be simplified and implemented with flexibility. Generally speaking, a `Pig` script follows the steps as the example shown below:
```piglatin
-- loading data
A = LOAD 'my_data.txt' USING PigStorage(',') AS (f1:int, f2:int);
-- processing
GP = GROUP A BY f1;
AVG_GP = FOREACH ...;
-- saving data
STORE AVG_GP INTO 'output' USING PigStorage(',');
```
*Snippet 1: A Pig Script Example*

### Parameter File
To avoid hardcoding and to gain the flexibility to handling different file paths, the scripts implemented use one parameter file which includes the essential paths for the inputs and outputs. More variables that are used by the scripts can also be added in the parameter file, too.

The parameter file content should match with `Perl` syntax and format, or it cannot be parsed by the `Pig` process. The below code snippet shows the file.
```perl
# file: parameter

# The input/output directories managed by HDFS
inputDir = '/p4/input'
outputDir = '/p4/output'
```
*Snippet 2: The Parameter File Content*

These 2 parameters are used by the scripts to locate the input files and the output result file. The below code snippet shows an example:
```piglatin
-- read in the data
actors = LOAD '$inputDir/actor.csv' USING PigStorage(',');
-- processing
A = ...;
-- Save the map/reduce result
STORE A INTO '$outputDir/query_result' USING PigStorage(',');
```

The following command shows how to run a script with a parameter file:
```bash
$ pig -param_file ./parameters -x mapreduce -f query_a_avg_length_by_category.pig
```
*Snippet 3: The Command with a Parameter File*

Alternatively, the scripts also can be run without the parameter file, but if it is the case, the parameters then must be given in the terminal commands that run the scripts. The below command demonstrates the way to run a script.
```bash
$ pig -param inputDir=/p4/input -param outputDir=/p4/output -x mapreduce -f query_a_avg_length_by_category.pig
```
*Snippet 4: The Command with Parameters*

### Class CSVExcelStorage
The data files for the input are typical `.csv` files which have column headers with the `CRLF` line endings. They cannot be processed directly by the built-in class `PigStorage` unless the columns headers are taken out.

The library `piggbank` has a class, `CSVExcelStorage`, which is capable of handling `.csv` files, with or without headers. So it's introduced to this project. `piggybank` is by default included by the `Pig` installation package, however it's not a built-in class. The full qualification name is required to use the class `CSVExcelStorage`. I.E.:
```piglatin
category = LOAD '$inputDir/category.csv'
           USING org.apache.pig.piggybank.storage.CSVExcelStorage(
               ',', 'NO_MULTILINE',
               'WINDOWS', 'SKIP_INPUT_HEADER')
           AS (category_id: int, name: chararray);
```
*snippet 5: Using `CSVExcelStorage` to load the data.*

### Query A
This problem is asking for a sequence of queries which in the end generate a list of the categories with the average length of films. The involved data files are `category.csv`, `film_category.csv` and `film.csv`.

The below code snippet shows a few lines of the script:
```piglatin
category = LOAD '$inputDir/category.csv'
           USING org.apache.pig.piggybank.storage.CSVExcelStorage(
               ',', 'NO_MULTILINE',
                'WINDOWS', 'SKIP_INPUT_HEADER')
           AS (category_id: long, name: chararray);

film_category = LOAD '$inputDir/film_category.csv' ...;

film = LOAD '$inputDir/film.csv' ...;
-- films with categories
categorized_films = ...;
...;
-- compute the avg
categorized = GROUP categorized_films BY (category_id, category_name);
avg = FOREACH categorized
      GENERATE FLATTEN(group),
               ROUND_TO(AVG(categorized_films.film_length), 2) AS avg_length;
result = ORDER avg BY category_name;

STORE result INTO '$outputDir/query_a_result' ...;
```
*Snippet 6: Query A*

The below lines shows the content captured from the result file:
```bash
category_name,  avg_film_length
-------------   ---------------
Action,         111.61
Animation,      111.02
Children,       109.8
Classics,       111.67
Comedy,         115.83
Documentary,    108.75
Drama,          120.84
Family,         114.78
Foreign,        121.7
Games,          127.84
Horror,         112.48
Music,          113.65
New,            111.13
Sci-Fi,         108.2
Sports,         128.2
Travel,         113.32
```
*Snippet 7: The Result of Query A*

### Query B
This problem is asking for a computed list of the film categories which have the longest average film length and the shortest average film length. The involved data files are `category.csv`, `film_category.csv`, `film.csv`.

The below code snippet shows a few lines of the script:
```piglatin
category = LOAD '$inputDir/category.csv' ...;

film_category = LOAD '$inputDir/film_category.csv' ...;

film = LOAD '$inputDir/film.csv' ...;
-- films with categories
categorized_films = ...;
...;
avg = FOREACH ...;
-- get max/min
min_avg = LIMIT (ORDER avg BY avg_length) 1;
max_avg = LIMIT (ORDER avg BY avg_length DESC) 1;

set default_parallel 1;
result = UNION max_avg, min_avg;
--gpResult = GROUP result BY 1;
finalResult = FOREACH (GROUP result BY 1)
              GENERATE FLATTEN(result)
              AS (category_id, category_name, avg_length);

STORE finalResult INTO '$outputDir/query_b_result' ...;
```
*Snippet 8: Query B*

The below lines shows the content captured from the result file:
```bash
category_id,    category_name,  avg_length
------------    --------------  ----------
14,             Sci-Fi,         108.2
15,             Sports,         128.2
```
*Snippet 9: The Result of Query B*

### Query C
This problem is asking for a list of customers who have rented action movies but not comedy or classic movies. The involved data files are `rental.csv`, `customer.csv`, `inventory.csv`, `film.csv`, `film_category.csv`, `category.csv`.

The below code snippet shows a few lines of the script:
```piglatin
-- prepare the information needed
...;
-- customers who have not rented 'Comedy' or 'Classics'
customers_rented_comedy_classic = FILTER customer_film_info BY category_name MATCHES '^(Comedy|Classics).*$';
-- customers who have rented 'Action' out of customers_not_rented_comedy_classic
customers_rented_action = FILTER customer_film_info BY category_name MATCHES '^(Action)$';
-- use left join to get the difference betwee customers_rented_comedy_classic and customers_rented_action
customers_action_in_comedy_classic = JOIN customers_rented_action BY customer_id LEFT,
                                          customers_rented_comedy_classic BY customer_id USING 'replicated';
-- customers who have rented 'ACTION' but not 'Comedy' or 'Classics'
customers_info = DISTINCT (FILTER customers_action_in_comedy_classic BY customers_rented_comedy_classic::customer_id is null);
customers_final = FOREACH ...;
customers_final_ordered = ...;

STORE customers_final_ordered INTO '$outputDir/query_c_result' ...;
```
*Snippet 10: Query C*

The below lines shows the content captured from the result file:
```text
customer_id,    first_name, last_name
------------    ----------- ---------
433,            DON,        BONE
432,            EDWIN,      BURK
139,            AMBER,      DIXON
223,            MELINDA,    FERNANDEZ
445,            MICHEAL,    FORMAN
250,            JO,         FOWLER
350,            JUAN,       FRALEY
164,            JOANN,      GARDNER
361,            LAWRENCE,   LAWTON
323,            MATTHEW,    MAHAN
452,            TOM,        MILNER
232,            CONSTANCE,  REID
330,            SCOTT,      SHELLEY
17,             DONNA,      THOMPSON
171,            DOLORES,    WAGNER
90,             RUBY,       WASHINGTON
213,            GINA,       WILLIAMSON
```
*Snippet 11: The Result of Query C*

### Query D
This problem is asking for a list of actors who have appeared in the most English-language movies. The involved data files are `film_actor.csv`, `actor.csv`, `film.csv`, `language.csv`.

The below code snippet shows a few lines of the script:
```piglatin
english = FILTER language BY name MATCHES '^English$';
english_films = JOIN film BY language, english by language_id USING 'replicated';
english_film_actors = JOIN film_actor BY film_id, english_films by film::film_id USING 'replicated';
actor_films_counts = FOREACH (GROUP english_film_actors BY film_actor::actor_id)
                     GENERATE group AS actor_id,
                              COUNT(english_film_actors) AS actor_count;
actor_max_film_count = LIMIT (ORDER actor_films_counts BY actor_count DESC) 1;
which_actor = JOIN actor_max_film_count BY actor_id, actor BY actor_id USING 'replicated';
result = FOREACH which_actor ...;

STORE result INTO '$outputDir/query_d_result' ...;
```
*Snippet 12: Query D*

The below lines shows the content captured from the result file:
```text
actor_id,   first_name, last_name
---------   ----------- ---------
107,        GINA,       DEGENERES
```
*Snippet 13: The Result of Query D*

### Query E
This problem is asking for the count of the distinct movie names which were rented for exactly 10 days from store(s) that Mike works. Therefore by the analysis, there are 4 data files involved, which are `film.csv`, `inventory.csv`, `rental.csv`,  `staff.csv`.

The below code snippet shows a few lines of the script:
```piglatin
staff = LOAD '$inputDir/staff.csv' ...;
film = LOAD '$inputDir/film.csv' ...;
inventory = LOAD '$inputDir/inventory.csv' ...;
rental = LOAD '$inputDir/rental.csv' ...;

rented_w_days = ...;
-- rented films for 10 days
rented_10d = FILTER rented_w_days BY DaysBetween(return_date,  rental_date) == 10;
-- get Mike's store and inventory
mike = FILTER staff BY (fname MATCHES '^Mike$');
stores_mike_inventory = ...;
-- films that were rented in the store that Mike works
rented_mike_store_10d = ...;
films_10d = FOREACH rented_mike_store_10d
            GENERATE stores_mike_inventory::film_id AS film_id;
-- get unique ids
unique_films_10d = ...;
-- get the count
final = FOREACH (GROUP unique_films_10d ALL)
        GENERATE COUNT(unique_films_10d);

STORE final INTO '$outputDir/query_e_result'...;
```
*Snippet 14: Query E*

The below lines shows the content captured from the result file:
```bash
count of films
--------------
61
```
*Snippet 15: The Result of Query E*

### Query F
This problem is asking for an ordered list of the actor names. The data files involved are `film_actor.csv`, `actor.csv`

The below code snippet shows a few lines of the script:
```piglatin
film_actors = LOAD '$inputDir/film_actor.csv' ...;

actors = LOAD '$inputDir/actor.csv' ...;

-- group film_actors with actor counts
actor_counts = FOREACH (GROUP film_actors BY film_id)
               GENERATE
                   group as film_id:long,
                   COUNT(film_actors) as actor_count:long;

sorted_actor_counts = ... ; -- sort film group by actor counts
max_actor_counts = LIMIT sorted_actor_counts 1;

films_max_actor_counts = ...; -- film ids which have the max count of actors
-- get the actors in the films from films_max_actor_counts
actor_ids = DISTINCT (FOREACH (
                        JOIN film_actors BY film_id,
                             films_max_actor_counts BY film_id)
                      GENERATE ... );
-- generate actor names
actor_names = FOREACH (JOIN actors BY actor_id, actor_ids BY actor_id)
              GENERATE ...;

ordered_actors = ...; -- order the names

STORE final INTO ...; -- saving the result
```
*Snippet 16: Query F*

The below lines shows the content captured from the result file:
```bash
actor_id,   first_name, last_name
---------   ----------- ---------
47,         JULIA,      BARRYMORE
37,         VAL,        BOLGER
81,         SCARLETT,   DAMON
138,        LUCILLE,    DEE
28,         WOODY,      HOFFMAN
170,        MENA,       HOPPER
45,         REESE,      KILMER
61,         CHRISTIAN,  NEESON
150,        JAYNE,      NOLTE
75,         BURT,       POSEY
53,         MENA,       TEMPLE
102,        WALTER,     TORN
147,        FAY,        WINSLET
111,        CAMERON,    ZELLWEGER
186,        JULIA,      ZELLWEGER
```
*Snippet 17: The Result of Query F*

## Running the Pig Latin Scripts
The scripts should run in `mapreduce` mode to use `HDFS` and `Yarn`. Hence, the input data files must be managed by `HDFS`.

> Assumptions:
> 1. On the `NameNode`, there is a user named as `hduser` who has proper permissions to run `Hadoop`'s services/daemons/commands.
> 1. The [Apache Pig Latin][pig_releases] subsystem for `Hadoop` has been installed
> 1. All the files and subdirectories of this project are uploaded and reside under `/home/hduser/p4` on the `NameNode`.

Take the following steps to configure and run the scripts:
1. Log into the `NameNode`
1. Create the input/output directories for this project in `HDFS`:
    ```bash
    $ hdfs dfs -mkdir /p4
    $ hdfs dfs -mkdir /p4/input
    $ hdfs dfs -mkdir /p4/output
    ```
1. Upload all `.csv` data files to `HDFS`, to `/p4/input`:
    ```bash
    $ hdfs dfs -put /home/hduser/p4/input/*.csv /p4/input
    ```
1. Edit `/home/hduser/p4/src/parameters` to set the `$inputDir` and `$outputDir` variables, which is shown below:
    ```perl
    # file: parameters
    # This file contains the variables that are used by the Pig scripts.

    # The input/output directories managed by HDFS
    inputDir = '/p4/input'
    outputDir = '/p4/output'
    ```
1. Run the scripts by using `pig` command, i.e.:
    ```bash
    $ pig -param_file /home/hduser/p4/src/parameters -x mapreduce -f /home/hduser/p4/src/query_a_avg_length_by_category.pig
    ```
    The result is saved under `/p4/output/query_a_result`, the result file has already been saved in `csv` format with column headers, thus it can be directly renamed to a `.csv` name:
    ```bash
    $ hdfs dfs -get /p4/output/query_a_result/part-r-00000 .
    $ mv part-r-00000 ./query_a.csv
    $ less query_a.csv
    ```
1. To rerun the scripts, the result subdirectories in `HDFS` must be removed:
    ```bash
    $ hdfs dfs -rm -r /p4/output/*
    ```

# About Team 1
Team 1 consists of three members, who are:
+ Jason Qiao Meng *(Team Lead)*
+ Sarah Cooney *(Developer)*
+ Mingyuan Li *(Developer)*

<!-- Reference links -->
[apache_hadoop]: http://hadoop.apache.org/  "Apache Hadoop Project Home"
[hadoop_releases]: http://hadoop.apache.org/releases.html "Apache Hadoop Releases"
[pig_getstarted]: http://pig.apache.org/docs/r0.16.0/start.html#Pig+Setup "Getting Started"
[pig_releases]: http://hadoop.apache.org/pig/releases.html "PIG Releases"
[ranking]: ranking.html "Team Member Efforts & Contributions"
[pig_latin]: https://pig.apache.org/ "Apache Pig Latin Home"
