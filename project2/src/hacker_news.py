#!/usr/bin/env python
#
# Copyright 2017 team1@course_bigdata, Saint Joseph's University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# google bigquery
from google.cloud import bigquery
from google.cloud.bigquery import Dataset, Table
# project home brews
from settings import GOOG_PROJECT_ID, GOOG_DATASET_NAME
from settings import \
    STORY_COUNT_TABLE_NAME, LOWEST_SCORE_TABLE_NAME, \
    BEST_STORY_URL_AVG_TABLE_NAME, STORY_COUNT_PER_AUTHOR
from bigquery import BigQuery

__doc__ = """This module includes helper functions for the big queries to Hacker News.
Developers shall implement the query function here to separate such from the web controllers.
The controllers shall be implemented in other modules/classes.
"""


def __get_project_dataset():
    """Get the project dataset defined by settings.GOOG_DATASET_NAME,
     or create the dataset if it does not exist yet.

    :return: The project dataset instance.
    """
    return None


def __get_project_table(name, dataset):
    """Get the desired table, or create it if it does not exist yet.

    :param name: string The name of the table
    :param dataset: An instance of the class bigquery.
    :type name: str
    :type dataset: Dataset
    :return: Return an instance of class bigquery.Table
    :rtype: Table
    """
    if not dataset or not name:
        return None

    t = dataset.table(name)
    if not t.exists():
        t.create()

    return t
