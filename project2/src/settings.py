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

"""This file is the base configuration which keeps the CONSTANTS."""

# The source connection string for Hacker News
GOOG_HACKER_NEWS_TABLE_FULL = r'full'
GOOG_HACKER_NEWS_TABLE_STORIES = r'stories'
GOOG_HACKER_NEWS_SOURCE = r'hacker_news'
GOOG_PUBLIC_DATA_PROJ_ID = r'bigquery-public-data'
# The google service secret variable name
GOOG_CREDENTIALS_ENV_VAR = 'GOOGLE_APPLICATION_CREDENTIALS'

# The data table name
STORY_COUNT_TABLE_NAME = 'table_a'
LOWEST_SCORE_TABLE_NAME = 'table_b'
BEST_STORY_URL_AVG_TABLE_NAME = 'table_c'
STORY_COUNT_PER_AUTHOR = 'table_d'

import os
# To override base settings values
# if some are redefined in the cust_settings.py
from cust_settings import *

# Create/set the environment variable for the google service credentials
if GOOG_CREDENTIALS_ENV_VAR not in os.environ:
    os.environ[GOOG_CREDENTIALS_ENV_VAR] = GOOG_CREDENTIALS_FILE_PATH
