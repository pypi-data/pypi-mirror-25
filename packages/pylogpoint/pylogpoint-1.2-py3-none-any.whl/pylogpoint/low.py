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

import json
import urllib

import requests

# Guesstimate of a sane value
DEFAULT_TIMEOUT = 60


class LowLevelAPI:
    def __init__(self, base_url, username, secret_key, verify_certificate=True):
        self.base_url = base_url
        self.username = username
        self.secret_key = secret_key
        self.verify_certificate = verify_certificate

    def _make_api_call(self, url_end_point, request_data, timeout=None):
        if not timeout:
            timeout = DEFAULT_TIMEOUT

        url = urllib.parse.urljoin(self.base_url, url_end_point)

        payload = request_data.copy()
        payload['username'] = self.username
        payload['secret_key'] = self.secret_key

        response = requests.post(
            url, data=payload, timeout=timeout, verify=self.verify_certificate)
        response.raise_for_status()
        response_data = response.json()

        if not response_data['success']:
            default_msg = "No failure message returned by LogPoint API: {}"
            msg = response_data.get(
                'message', default_msg.format(response_data))
            raise ApiCallFailure(msg)

        return response_data

    def get_allowed_data(self, type_, timeout=None):
        return self._make_api_call('/getalloweddata', {'type': type_}, timeout)

    def get_search_logs(self, request_data, timeout=None):
        request_data_str = json.dumps(request_data)

        return self._make_api_call(
            '/getsearchlogs', {'requestData': request_data_str}, timeout)


class ApiCallFailure(Exception):
    pass
