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

"""This module includes the variable for server side routes for the requests.
"""


# The server side redirection is defined here
ROUTES = [
    # (route/path, handler class full name)
    (r'/reset', 'reset.Reset'),
    (r'/authorKPI', 'story_count_by_author_on_domain.StoryCountByAuthorOnDomain'),
    (r'/storyCount', 'total_story_producer.TotalStoryCount'),
    (r'/lowestScoreStory', 'lowest_story_score.LowestStoryScore'),
    (r'/avgBestStoryProducer', 'avg_best_story_producer.BestStoryProducerAVG'),
    (r'/', 'index.MainHandler')
]
