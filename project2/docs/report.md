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

<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>

# Project 2: Playing with Hacker News Data


*This project is developed by* ***Team 1***:
* Sarah Cooney
* Mingyuan Li
* Jason Qiao Meng

<div class="page-break"></div>

## Table of Content

<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>

## Introduction
This project is developed in Python. It is built on top of [WebApp2][webapp2] framework with the standard [Python Client API Libraries][goog_py_cli_api] to access to Google's backend public datasets.

The application developed in this project allows web clients to process the following form-driven queries:
+ How many stories are there?
+ Which story has received the lowest score?
+ On average which URL produced the best story in 2010?
+ List how many stories where posted by each author on nytimes.com and wired.com.

*For team member contributions, see: [workload and responsibilities][ranking]*

### License
*Apache License V2.0* is applied to this project.

## Implementation
This project implements a lightweight web application which is designed for [WebApp2][webapp2] framework and to be driven by [Google App Engine][goog_python_app_engine].

The implementation incorporates `Google Cloud BigQuery` library to execute some simple queries towards Google's public data set `Hacker News`, and display the query results on a HTML template.

The source consists of 2 parts:
+ A wrapper class `BigQuery` which provides major features to facilitate query execution. Such class masks out the complexity of library `google.cloud.bigquery`.
+ A web application which conforms to the convention of [WebApp2][webapp2] and [Google App Engine][goog_python_app_engine], and which handles the requests from the web clients.

### Technical Architecture
The architecture of this application is designed on top of [WebApp2][webapp2] and [Google App Engine][goog_python_app_engine].

#### Overview
![alt text](architeture.png "The project architecture")

#### Class Diagram
// TODO

#### Sequence Diagram
The following diagram example demonstrates how the post request is handled by this App.
![alt text](sequence.png "The project architecture")

### Connecting to Hacker News Public Data Set
The connection to the `hacker news` public data set is managed by the class `BigQuery` which is enclosed by the `Python` source file `bigquery.py`.

The method `get_client()`, as figure 1 shows, creates a `Google BigQuery API` client with the service credentials defined by the settings variables `GOOG_CREDENTIALS_ENV_VAR` and `GOOG_CREDENTIALS_FILE_PATH`. See the section [Configuration](#configuration) for more information.
```python
    def get_client(self):
        """Get a client of the big query service.

        :return: An instance of a client of bigquery service
        :rtype: bigquery.Client
        """
        self.__cli = self.__cli if self.__cli else bigquery.Client(self.__proj)
        return self.__cli
```
*Figure 1: `get_client()` to create a `Google BigQuery Client` object.*


### Global Settings

### Features

## Running the App
This web app is development for [Google App Engine][goog_python_app_engine]. It can run locally without `Google Cloud Platform`'s `standard environment`.
However there are a few things to be done before the app can be run.

### Prerequisites
Make sure the following software packages are installed.

#### Google Cloud SDK and App Engine
+ Download and install the `Google Cloud SDK` from https://cloud.google.com/sdk/docs/.
+ Initialize the `Google Cloud Client` environment by using the following command:
```cmd
X:\> gcloud init
```
+ Install [Google App Engine][goog_python_app_engine] by using the following commands:
```cmd
X:\> gcloud components install app-engine-python
X:\> gcloud components install app-engine-python-extras
```

#### Python Libraries Required
Go to the project's `src` directory, make a sub directory named `lib`, and apply the following commands:
```cmd
X:\> pip install -U -t lib/ google-api-python-client
X:\> pip install -U -t lib/ google-cloud-bigquery
```

#### Google Cloud Project
A valid `Google Cloud` project is used by this app.

+ Go to [Google Cloud Console](https://console.cloud.google.com) and make sure there is a functional project.
+ Go to `IAM & Admin` page of the `Google Cloud Console`, assign `Bigquery > Data Owner` role to the service account.

### Configuration
Before the app can be driven by the [Google App Engine][goog_python_app_engine], A few changes should be made for the project to adapt to the local environment.

Open `cust_settings.py`, set the proper values to the following variables:
```python
# The google project id - Place your project id here
GOOG_PROJECT_ID = r'<project_id>'
# The google service credentials.
GOOG_CREDENTIALS_FILE_PATH = r'<service_account_secret_json_file>'
# The dataset name
GOOG_DATASET_NAME = r'<dataset_id>'
```

### Launching The App
Use the following command to run the web app:
```cmd
X:\<project_root>\src\> dev_appserver.py app.yaml
```

# About Team 1
Team 1 consists of three members, who are:
+ Jason Qiao Meng *(Team Lead)*
+ Sarah Cooney *(Developer)*
+ Mingyuan Li *(Developer)*

<!-- Reference links -->
[goog_bigquery]: https://cloud.google.com/bigquery/docs/  "Google BigQuery Documentation"
[bigtable_hacker_news]: https://cloud.google.com/bigquery/public-data/hacker-news "Hacker News Data"
[goog_python_app_engine]: https://cloud.google.com/appengine/docs/standard/python/ "Google App Engine Python Standard Environment Documentation"
[webapp2]: https://cloud.google.com/appengine/docs/standard/python/tools/webapp2 "The webapp2 Framework"
[goog_py_cli_api]: https://developers.google.com/api-client-library/python/ "Google Python Client API"
[ranking]: ranking.html "Team Member Efforts & Contributions"
