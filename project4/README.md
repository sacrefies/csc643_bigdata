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

# The Project
This project is the final project of CSC643.

This project works with the [Apache Pig Latin][pig_latin] and the [Apache Hadoop][apache_hadoop]. It is about a set of `Pig Latin` scripts which are to be executed on a `Hadoop` cluster of 2. The scripts produce results for the following problems:
1. What is the average length of films in each category? List the results in alphabetic order of categories.
1. Which categories have the longest and shortest average film lengths?
1. Which customers have rented action but not comedy or classic movies?
1. Which actor has appeared in the most English-language movies?
1. How many distinct movies were rented for exactly 10 days from the store where Mike works?
1. Alphabetically list actors who appeared in the movie with the largest cast of actors.


*See the [project report](docs/report.md) for details.*

## Pig Latin Installation
Please see [Install and Set-up Apache Pig Latin](docs/set_up_pig.md) document.

## Running the Scripts
The scripts should run in `mapreduce` mode to use `HDFS` and `Yarn`. Hence, the input data files must be managed by `HDFS`.

> Assumptions:
> 1. On the `NameNode`, there is a user named as `hduser` who has proper permissions to run `Hadoop`'s services/daemons/commands.
> 1. The [Apache Pig Latin][pig_releases] subsystem for `Hadoop` has been installed
> 1. All the files and subdirectories of this project are uploaded and reside under `/home/hduser/p4` on the `NameNode`.

Take the following steps to config and run the scripts:
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

<!-- Reference links -->
[apache_hadoop]: http://hadoop.apache.org/  "Apache Hadoop Project Home"
[hadoop_docs]: http://hadoop.apache.org/docs/r2.7.3/  "Apache Hadoop 2.7.3 Documentation"
[pig_latin]: https://pig.apache.org/ "Apache Pig Latin Home"
