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


"""This module includes view controller class for the query D:
  - List how many stories where posted by each author on nytimes.com and wired.com.
"""

# built-in libs
import os
# google/webapp2 libs
import webapp2
from google.appengine.ext.webapp import template
# homemade ones
import hacker_news as hacker


class StoryCountByAuthorOnDomain(webapp2.RequestHandler):
    def post(self):
        rows, count = hacker.get_wired_and_nyt_counts()
        temp_vals = {
            'active_tab': 'QueryD',
            'total_count': count,
            'values': rows if rows else None
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(path, temp_vals))
