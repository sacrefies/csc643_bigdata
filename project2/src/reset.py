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

"""This file includes variables for the values that configurable and changing.
Developers shall keep their own versions locally for their own development environments.
The values of the variables will be set to different values for the runtime environment.
"""

import os
import webapp2
from google.appengine.ext.webapp import template
import hacker_news as hacker


class Reset(webapp2.RequestHandler):
    def get(self):
        hacker.reset()
        self.redirect('/')
