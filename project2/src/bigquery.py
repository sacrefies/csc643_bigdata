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


"""This module includes a base class which wraps the Google Cloud BigQuery
library.

By using the class ``BigQuery``, the invoker can proceed with:
    + Get a bigquery cloud service client
    + Perform a synchronous query
    + Perform an asynchronous query
    + Get a dataset
    + Create a dataset
    + Create a table
    + Auxiliary funcions:
        + Construct SQL's parameters
        + Construct table schema

Example 1 - Create the project dataset::

    from bigquery import BigQuery

    bq = BigQuery()
    ds = bq.get_dataset()
    if not ds.exists():
        ds = bq.create_dataset()

Example 2 - Create a table::

    from bigquery import BigQuery

    bq = BigQuery()
    bq.get_dataset()

    cols = {
        'name': 'STRING',
        'Age': 'INTEGER',
    }
    schema = BigQuery.build_schema(cols)
    t = bq.create_table('table_a', cols)

Example 3 - Perform a query::

    from bigquery import BigQuery

    sql = \"""
        SELECT word, word_count
        FROM %s
        WHERE corpus = @corpus
        AND word_count >= @min_word_count
        ORDER BY %s DESC;
    \""" % ('`bigquery-public-data.samples.shakespeare`', 'word_count')

    bq = BigQuery()
    bq.get_client()
    rs, total = bq.sync_query(sql,
"""

# built-in libs
import time
import uuid
# google bigquery
from google.cloud import bigquery
# project home brews
from settings import GOOG_PROJECT_ID, GOOG_DATASET_NAME, MAX_RESULT_COUNT


class BigQuery(object):
    """A helper class to wrap up Google BigQuery library.

    Usage::

        bq = BigQuery()
        # get a dataset handler under the default project
        # the default project == settings.GOOG_PROJECT_ID
        ds = bq.get_dataset('my_dataset')
        # create the dataset
        ds.create()
        # do a query
        rs, row_count = bq.sync_query(r'SELECT * FROM [bigquery-public-data:samples.gsod] LIMIT 10')
        for row in rs:
            print rs
    """

    def __init__(self, project=None):
        """Create and initialize an instance of class BigQuery.

        :param project: (Optional) The name of the project. If omitted, settings.GOOG_PROJECT_ID is used by default.
        :type project: str
        """
        self.__proj = project if project else GOOG_PROJECT_ID
        self.__cli = None
        self.__ds = None

    def get_client(self):
        """Get a client of the big query service.

        :return: An instance of a client of bigquery service
        :rtype: bigquery.Client
        """
        self.__cli = self.__cli if self.__cli else bigquery.Client(self.__proj)
        return self.__cli

    def get_dataset(self, name=None):
        """Get a dataset handler object.

        :param name: (Optional) The name of the dataset. If omitted, settings.GOOG_DATASET_NAME is used by default.
        :type name: str
        :return: An new instance of a Dataset.
        :rtype: bigquery.Dataset
        """
        self.get_client()

        name = name if name else GOOG_DATASET_NAME
        self.__ds = self.__ds if self.__ds and name == GOOG_DATASET_NAME else self.__cli.dataset(name)
        if self.__ds.exists():
            self.__ds.reload()
        return self.__ds

    def create_dataset(self, name=None):
        """Create a dataset.

        :param name: (Optional) The name of the dataset.
        :type name: str
        :return: Returns a dataset instance
        :rtype: bigquery.Dataset
        """
        self.get_dataset(name)
        if not self.__ds.exists():
            self.__ds.create()
            self.__ds.reload()
        return self.__ds

    def create_table(self, name, schema):
        """Create a table with the specified schema.

        :param name: The name of the table.
        :type name: str
        :param schema: The schema of the table. This schema can be built by the class function `build_schema()`.
        :type schema: dict
        :return: Return the table object that was created. Or return None if failed.
        :rtype: bigquery.Table
        """
        if not name or not schema:
            return None

        self.get_dataset()
        if not self.__ds.exists():
            return None

        t = self.__ds.table(name)
        if t.exists():
            return t
        t.schema = schema
        t.create()
        return t

    def sync_query(self, query, params=()):
        """Perform a query and return the result and the total count of the affected rows.
        To use the parameters, please refer to the example below::
            query_parameters=(
                bigquery.ScalarQueryParameter('corpus', 'STRING', corpus),
                bigquery.ScalarQueryParameter(
                    'min_word_count',
                    'INT64',
                    min_word_count))

        :param query: A Standard SQL that Google BigQuery accepts.
        :type query: str
        :param params: (Optional) The parameters that the query uses.
        :type params: tuple
        :return: Returns the result set (only values) and the total count of the affected rows.
        :rtype: tuple
        """
        self.__cli = self.get_client()
        query_results = self.__cli.run_sync_query(query, query_parameters=params)

        # Use standard SQL syntax for queries.
        # See: https://cloud.google.com/bigquery/sql-reference/
        query_results.use_legacy_sql = False
        query_results.run()
        # get all possible rows
        pt = None
        rs = []
        while True:
            row_data, total_rows, page_token = query_results.fetch_data(MAX_RESULT_COUNT, page_token=pt)
            rs += [row for row in row_data]
            if not page_token:
                break

        return rs, total_rows

    def async_query(self, query, params=(), dest_table=None, dest_dataset=None):
        """Perform a query *asynchronously* and return the result and the total count of the affected rows.
        To use the parameters, please refer to the example below::

            params = {
                'name': 'John',
                'age': 21,
                'married': False
            }
            converted_params = BigQuery.build_params(params)
            sql = \"""
                SELECT *
                FROM %s
                WHERE name = @name
                AND   age = @age
                AND   is_married = @married
                LIMIT %d
            \""" % ('`mydataset.sometable`', 10)
            bq = BigQuery()
            bq.get_client()
            rs, total = bq.async_query(query, converted_params)

        :param query: A Standard SQL that Google BigQuery accepts.
        :type query: str
        :param params: (Optional) The parameters that the query uses.
        :type params: tuple
        :param dest_table: (Optional) The name of the destination table where the job saves the result set.
        :type dest_table: str
        :param dest_dataset: (Optional) The name of the dataset which has the destination table.
                            If omitted, ``GOOG_DATASET_NAME`` is used by default.
        :type dest_dataset: str
        :return: Returns the result set (only values) and the total count of the affected rows.
        :rtype: tuple
        """
        self.__cli = self.get_client()
        query_job = self.__cli.run_async_query(str(uuid.uuid4()), query, query_parameters=params)
        query_job.use_legacy_sql = False
        if dest_table:
            ds = self.__cli.dataset(dest_dataset) if dest_dataset else self.get_dataset()
            tbl_save = ds.table(dest_table)
            query_job.destination = tbl_save
            # configuration.copy.writeDisposition
            # string [Optional] Specifies the action that occurs if the destination table already exists.
            #
            # The following values are supported:
            #
            # WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data.
            # WRITE_APPEND: If the table already exists, BigQuery appends the data to the table.
            # WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned
            # in the job result.
            #
            # The default value is WRITE_EMPTY.
            #
            # Each action is atomic and only occurs if BigQuery is able to complete the job successfully.
            # Creation, truncation and append actions occur as one atomic update upon job completion.
            query_job.write_disposition = 'WRITE_TRUNCATE' if tbl_save.exists() else 'WRITE_EMPTY'

        query_job.begin()
        # wait for the job complete
        BigQuery.__async_wait(query_job)

        # Drain the query results by requesting a page at a time.
        query_results = query_job.results()
        rs = []
        pt = None
        while True:
            row_data, total_rows, page_token = query_results.fetch_data(MAX_RESULT_COUNT, page_token=pt)
            rs += [row for row in row_data]
            if not page_token:
                break

        return rs, total_rows

    def transfer_from_query(self, dest_table, query, params=(), dest_dataset=None):
        """Run the given query, save the query result set into the destination table.
        This function has no return value.

        :param dest_table: The name of the table which is to save the query result set.
                           The table will be created automatically if it does not exists;
                           If The table exists, the existing data will be overwritten.
        :type dest_table: str
        :param query: The query to be executed.
        :type query: str
        :param params: (Optional) The parameters that the query uses.
        :type params: tuple
        :param dest_dataset: (Optional) The name of the dataset which has the destination table.
                            If omitted, ``GOOG_DATASET_NAME`` is used by default.
        :type dest_dataset: str
        """
        if not dest_table or not query:
            return

        self.__cli = self.get_client()
        ds = self.__cli.dataset(dest_dataset) if dest_dataset else self.get_dataset()
        tbl_save = ds.table(dest_table)

        trans_job = self.__cli.run_async_query(str(uuid.uuid4()), query, query_parameters=params)
        trans_job.use_legacy_sql = False
        trans_job.destination = tbl_save

        # configuration.copy.writeDisposition
        # string [Optional] Specifies the action that occurs if the destination table already exists.
        #
        # The following values are supported:
        #
        # WRITE_TRUNCATE: If the table already exists, BigQuery overwrites the table data.
        # WRITE_APPEND: If the table already exists, BigQuery appends the data to the table.
        # WRITE_EMPTY: If the table already exists and contains data, a 'duplicate' error is returned in the job result.
        #
        # The default value is WRITE_EMPTY.
        #
        # Each action is atomic and only occurs if BigQuery is able to complete the job successfully.
        # Creation, truncation and append actions occur as one atomic update upon job completion.
        trans_job.write_disposition = 'WRITE_TRUNCATE' if tbl_save.exists() else 'WRITE_EMPTY'

        trans_job.begin()
        # wait for the job complete
        self.__async_wait(trans_job)

    @classmethod
    def build_schema(cls, columns):
        """Construct a table's schema.

        Example::

            cols = {
                'name': 'STRING',
                'Age': 'INTEGER',
            }
            schema = BigQuery.build_schema(cols)

        :param columns: A dictionary which consists of {'name': 'BigQuery SQL type name'}
        :type columns: dict
        :return: Returns a tuple of schema objects.
        :rtype: tuple
        """
        return None if not columns else tuple([bigquery.SchemaField(k, v) for k, v in columns.iteritems()])

    @classmethod
    def build_params(cls, params):
        """Construct a tuple of the SQL parameters.

        `Note: this function produce scalar parameters only.`

        :param params: A ``python`` ``dict`` which holds the parameters
                       in form of {'name': value} where the value can be any object.
        :return: Returns a tuple of SQL parameter objects
        :rtype: tuple
        """
        if not params:
            return None

        def get_type(k, v):
            t = 'STRING'
            if isinstance(v, int):
                t = 'INT64'
            elif isinstance(v, float):
                t = 'FLOAT64'
            elif isinstance(v, bool):
                t = 'BOOL'
            return bigquery.ScalarQueryParameter(k, t, v)

        return tuple([get_type(key, value) for key, value in params.iteritems()])

    def __async_wait(self, job):
        """Wait for a job to finish.

        :param job: A `QueryJob` instance
        :type: :class:`google.cloud.bigquery.job.QueryJob`
        """
        if not job:
            return

        while True:
            # Refreshes the state via a GET request.
            job.reload()
            if job.state == 'DONE':
                if job.error_result:
                    raise RuntimeError(job.errors)
                return
            time.sleep(0.05)
