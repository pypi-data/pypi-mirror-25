# Copyright (c) 2017. The Language Applications Grid
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

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport


class ServiceClient:
    def __init__(self, uri):
        session = Session()
        session.auth = HTTPBasicAuth('tester', 'tester')
        transport = Transport(session=session)
        self.client = Client(uri, transport=transport)

    def get_metadata(self):
        return self.client.service.getMetadata();

    def execute(self, json):
        return self.client.service.execute(json)
