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

# built-in libs
import os
# webapp related libs
import webapp2
import paste.cascade as cascade
import paste.urlparser as paste_urlparser
# project includes
from settings import TEMPLATE_ENV


__doc__ = """Main entrance of this web app which plays as an 'index.html'
like in good old days.
"""


class TestMain(webapp2.RequestHandler):
    """This class is for testing.
    It behaves like an alternative site homepage.

    To Run
    ------
    $ python test.py
    """

    def get(self):
        """Response to a client http request
        """
        objects = os.listdir(os.curdir)
        # values to be bound to the template
        temp_vals = {
            'headline': 'Objects under the Current Folder',
            'objects': objects
        }
        template = TEMPLATE_ENV.get_template(r'test_general.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render(temp_vals))


app = webapp2.WSGIApplication(
    routes=[
        (r'/', TestMain),
    ],
    debug=True)

css_app = paste_urlparser.StaticURLParser('css/')
js_app = paste_urlparser.StaticURLParser('js/')
fonts_app = paste_urlparser.StaticURLParser('fonts/')

test_app = cascade.Cascade([css_app, app])


def main():
    print css_app.__repr__()
    from paste import httpserver
    httpserver.serve(test_app, host='127.0.0.1', port='8080')


# sanity test
if __name__ == '__main__':
    main()
