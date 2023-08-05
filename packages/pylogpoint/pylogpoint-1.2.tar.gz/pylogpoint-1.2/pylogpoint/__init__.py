#   Copyright 2017 University of Lancaster
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import time

from .low import LowLevelAPI

# Guesstimates
SEARCH_TIMEOUT = 900
MAXIMUM_SEARCH_UPDATE_FREQUENCY = 1


class LogPointSearchAPI:
    def __init__(self, base_url, username, secret_key, verify_certificate=True):
        self.low_level_api = LowLevelAPI(
            base_url, username, secret_key, verify_certificate)

    def get_user_preferences(self):
        return self.low_level_api.get_allowed_data("user_preference")

    def get_log_inspects(self):
        return self.low_level_api.get_allowed_data("loginspects")

    def get_repos(self):
        return self.low_level_api.get_allowed_data("logpoint_repos")

    def get_devices(self):
        return self.low_level_api.get_allowed_data("devices")

    def launch_search(self, query, limit, time_range, repos=None):
        request_data = {
            'timeout': SEARCH_TIMEOUT,
            'query': query,
            'limit': limit,
            'time_range': time_range,
            'repos': repos,
        }

        return self.low_level_api.get_search_logs(request_data)

    def get_search_results(self, search_id):
        request_data = {'search_id': search_id}
        return self.low_level_api.get_search_logs(request_data)

    def search(self, query, limit, time_range, repos=None):
        search_id = self.launch_search(
            query, limit, time_range, repos)['search_id']

        start_time = time.time()

        while start_time + SEARCH_TIMEOUT > time.time():
            search_time = time.time()

            results = self.get_search_results(search_id)

            if results['final']:
                return results

            pause_time = MAXIMUM_SEARCH_UPDATE_FREQUENCY - (time.time() - search_time)

            if pause_time > 0:
                time.sleep(pause_time)

        raise Timeout()


class Timeout(Exception):
    pass
