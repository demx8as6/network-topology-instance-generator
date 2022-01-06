# Copyright 2022 highstreet technologies GmbH
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

#!/usr/bin/python
import json

class NetworkViewer:

    network = {}

    # constructor
    def __init__(self, network):
        self.network = network
    
    # getter
    def getNetwork(self):
        return self.network
    
    def showAsJson(self):
      print(self.network)

    # json format
    def json(self):
      return self

    def show(self):
      print(self.getNetwork())

    def save(self, filename):
        with open(filename, "w", encoding='utf-8') as jsonFile:
            json.dump(self.network, jsonFile, ensure_ascii=False, indent=2)
