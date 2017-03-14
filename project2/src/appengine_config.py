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

"""This file is the overridden configurations for the Google App Engine.

To be able to use ``google.cloud.bigquery`` and other ``google.cloud`` libraries,
such google client api libs must be `vendor-ed` into this web app project.

:see: https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27#vendoring.

`Note`: Such ``lib`` sub-direction will be excluded from ``git``.
Developers should make and keep their own ``lib`` for the local ``AppEngine``.
"""

from google.appengine.ext import vendor

# Add any libraries install in the "lib" folder.
vendor.add('lib')
