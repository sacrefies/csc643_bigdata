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

<!-- Reference links -->
[apache_hadoop]: http://hadoop.apache.org/  "Apache Hadoop Project Home"
[hadoop_docs]: http://hadoop.apache.org/docs/r2.7.3/  "Apache Hadoop 2.7.3 Documentation"
[pig_latin]: https://pig.apache.org/ "Apache Pig Latin Home"
