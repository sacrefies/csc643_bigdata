# The Project
This project is an excise to use [Google BigQuery][goog_bigquery] and [Google App Engine][goog_python_app_engine] with [Hacker News Data][bigtable_hacker_news] on Google Cloud.

This project is developed in `Python 2.7.x` and utilizes [WebApp 2][webapp2] as the web application framwork which is supported by [Google App Engine][goog_python_app_engine].

## Content
- [Running the Web App](#running-the-web-app)
    - [Prerequisites](#prerequisites)
        - [Google Cloud SDK and App Engine](#google-cloud-sdk-and-app-engine)
        - [Python Libraries Required](#python-libraries-required)
        - [Google Cloud Project](#google-cloud-project)
    - [Configuration](#configuration)
    - [Launching The App](#launching-the-app)

# Running the Web App
This web app is development for [Google App Engine][goog_python_app_engine]. It can run locally without `Google Cloud Platform`'s `standard environment`.
However there are a few things to be done before the app can be run.

## Prerequisites
Make sure the following software packages are installed.

### Google Cloud SDK and App Engine
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

### Python Libraries Required
Go to the project's `src` directory, make a sub directory named `lib`, and apply the following commands:
```cmd
X:\> pip install -U -t lib/ google-api-python-client
X:\> pip install -U -t lib/ google-cloud-bigquery
```

### Google Cloud Project
A valid `Google Cloud` project is used by this app.

+ Go to [Google Cloud Console](https://console.cloud.google.com) and make sure there is a functional project.
+ Go to `IAM & Admin` page of the `Google Cloud Console`, assign `Bigquery > Data Owner` role to the service account.

## Configuration
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

## Launching The App
Use the following command to run the web app:
```cmd
X:\project_root\src\> dev_appserver.py app.yaml
```

<!-- Reference links -->
[goog_bigquery]: https://cloud.google.com/bigquery/docs/  "Google BigQuery Documentation"
[bigtable_hacker_news]: https://cloud.google.com/bigquery/public-data/hacker-news "Hacker News Data"
[goog_python_app_engine]: https://cloud.google.com/appengine/docs/standard/python/ "Google App Engine Python Standard Environment Documentation"
[webapp2]: https://cloud.google.com/appengine/docs/standard/python/tools/webapp2 "The webapp2 Framework"
