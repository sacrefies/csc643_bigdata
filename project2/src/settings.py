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

import os
import jinja2

__doc__ = """This file is the base configuration which keeps the CONSTANTS."""

# The source connection string for Hacker News
GOOG_HACKER_NEWS_SOURCE = r''
# The google service secret variable name
GOOG_CREDENTIALS_ENV_VAR = 'GOOGLE_APPLICATION_CREDENTIALS'

# To use the template framework, this global constant must be set.
TEMPLATE_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# To override base settings values
# if some are redefined in the cust_settings.py
from cust_settings import *

# Create/set the environment variable for the google service credentials
os.environ[GOOG_CREDENTIALS_ENV_VAR] = GOOG_CREDENTIALS_FILE_PATH
