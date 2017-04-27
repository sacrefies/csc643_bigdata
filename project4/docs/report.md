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
By using the [Apache Pig Latin][pig_releases], the `Hadoop` map/reduce process can be abstracted and transformed to a script in the relation algebra style. In this fashion, a map/reduce process can be simplified and implemented with flexibility. Generally speaking, a `Pig` script follows the below procedure:
```piglatin
-- loading data
A = LOAD 'my_data.txt' USING PigStorage(',') AS (f1:int, f2:int);
-- processing
GP = GROUP A BY f1;
AVG_GP = FOREACH GP GENERATE
               group AS g:int,
               AVG(A.$1) AS f2_avg:double;
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
...
-- Save the map/reduce result
STORE actors INTO '$outputDir/query_result' USING PigStorage(',');
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
           AS (category_id: int, name: chararray);

film_category = LOAD '$inputDir/film_category.csv' ...

film = LOAD '$inputDir/film.csv' ...

x = ...  -- join the data sets

gp = GROUP x BY (category_id, category_name);

avg = ... -- calculate the averages

STORE avg INTO '$outputDir/query_a_result';
USING org.apache.pig.piggybank.storage.CSVExcelStorage(',', 'NO_MULTILINE', 'UNIX', 'WRITE_OUTPUT_HEADER');
```

The below snippet shows a few sample lines captured from the result file:
```csv
```

### Query B

### Query C

### Query D

### Query E

### Query F


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
