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
# project home brews
from settings import GOOG_PROJECT_ID, GOOG_DATASET_NAME


__doc__ = """This module includes a base class which wraps the Google Cloud BigQuery
library
"""


class BigQuery(object):
    """A helper class to wrap up Google BigQuery library.

    Usage
    -----
    bq = BigQuery()
    # get a dataset handler under the default project
    # the default project == settings.GOOG_PROJECT_ID
    ds = bq.get_dataset('my_dataset')
    # create the dataset
    ds.create()
    """

    def __init__(self, project=None):
        """Create and initialize an instance of class BigQuery.

        :param project: The name of the project. If omitted, settings.GOOG_PROJECT_ID is used by default.
        """
        self.__proj = project if project else GOOG_PROJECT_ID
        self.__cli = bigquery.Client(self.__proj)
        self.__ds = None

    def get_dataset(self, dataset=None):
        """Get a dataset handler object.

        :param dataset: The name of the dataset. If omitted, settings.GOOG_DATASET_NAME is used by default.
        :return: A bigquery.Dataset object instance
        """
        self.__ds = self.__cli.dataset(dataset) if dataset else self.__ds \
            if self.__ds else self.__cli.dataset(GOOG_DATASET_NAME)

        return self.__ds

    def get_table(self, table, dataset=None):
        """Get a table handler object.

        :param dataset: The name of the dataset. If omitted, settings.GOOG_DATASET_NAME is used by default.
        :param table: The table name
        :return: A new instance of class bigquery.Table
        """
        if not table:
            return None

        self.__ds = self.get_dataset(dataset)
        return self.__ds.table(table)
