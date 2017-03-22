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

"""This module includes helper functions for the big queries to Hacker News.
Developers shall implement the query function here to separate such from the web controllers.
The controllers shall be implemented in other modules/classes.
"""

# built-in libs
from string import Template
# project home brews
from settings import GOOG_PROJECT_ID, GOOG_DATASET_NAME, \
    GOOG_PUBLIC_DATA_PROJ_ID, GOOG_HACKER_NEWS_SOURCE, GOOG_HACKER_NEWS_TABLE_STORIES, GOOG_HACKER_NEWS_TABLE_FULL, \
    STORY_COUNT_TABLE_NAME, LOWEST_SCORE_TABLE_NAME, \
    BEST_STORY_URL_AVG_TABLE_NAME, STORY_COUNT_PER_AUTHOR
from bigquery import BigQuery


def get_story_count():
    sql = """
        SELECT COUNT(id) AS storyCount
        FROM `$proj.$ds.$table`
    """
    sub = {
        'proj': GOOG_PUBLIC_DATA_PROJ_ID,
        'ds': GOOG_HACKER_NEWS_SOURCE,
        'table': GOOG_HACKER_NEWS_TABLE_STORIES
    }

    bq = BigQuery()
    bq.get_client()
    bq.transfer_from_query(STORY_COUNT_TABLE_NAME, Template(sql).substitute(sub))

    # fetch the data from the saving table
    sql = """
         SELECT *
         FROM $ds.$table ORDER BY $col DESC
       """
    sub = {
        'ds': GOOG_DATASET_NAME,
        'table': STORY_COUNT_TABLE_NAME,
        'col': 'storyCount'
    }
    return bq.sync_query(Template(sql).substitute(sub))[0]


def best_story_producer_on_avg():
    sql = """
        SELECT url, AVG(score) AS avgScore
        FROM `$proj.$ds.$table`
        WHERE
            TYPE = @type
        AND TIMESTAMP <= @end_date
        AND TIMESTAMP >= @start_date
        GROUP BY url
        HAVING avgScore >= (
          SELECT AVG(score) AS score
          FROM `$proj.$ds.$table`
          WHERE
              TYPE = @type
          AND url IS NOT NULL
          AND url <> ''
          AND TIMESTAMP <= @end_date
          AND TIMESTAMP >= @start_date
          GROUP BY url
          ORDER BY score DESC
          LIMIT 1 )
    """
    sub = {
        'proj': GOOG_PUBLIC_DATA_PROJ_ID,
        'ds': GOOG_HACKER_NEWS_SOURCE,
        'table': GOOG_HACKER_NEWS_TABLE_FULL
    }
    params = {
        'type': 'story',
        'start_date': '2010-01-01 00:00:01',
        'end_date': '2010-12-31 23:59:59'
    }
    p = BigQuery.build_params(params)

    bq = BigQuery()
    bq.get_client()
    bq.transfer_from_query(BEST_STORY_URL_AVG_TABLE_NAME, Template(sql).substitute(sub), p)

    # fetch the data from the saving table
    sql = """
      SELECT *
      FROM $ds.$table ORDER BY $col DESC
    """
    sub = {
        'ds': GOOG_DATASET_NAME,
        'table': BEST_STORY_URL_AVG_TABLE_NAME,
        'col': 'avgScore'
    }
    return bq.sync_query(Template(sql).substitute(sub))[0]


def reset():
    bq = BigQuery()
    bq.get_client()
    ds = bq.get_dataset()
    if ds.exists():
        for t in ds.list_tables():
            t.delete()
        ds.reload()
        ds.delete()
    ds.create()
