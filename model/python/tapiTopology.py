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
import uuid
from model.python.tapiNodeSmo import TapiNodeSmo


class TapiTopology:

    topology = {}

    # constructor
    def __init__(self, config):
        self.topology = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "network-name",
                "value": config['network']['name']}],
            "node": [],
            "link": []}
        topoStructure = config['network']['pattern']
        for networkFunctionType, count in config['network']['pattern'].items():
            print(networkFunctionType, count)
            if networkFunctionType == "smo":
                self.createSmos(topoStructure, count)
            elif networkFunctionType == "near-rt-ric":
                self.createNearRtRics(topoStructure, count)
            elif networkFunctionType == "o-cu":
                self.createOCus(topoStructure, count)
            elif networkFunctionType == "o-du":
                self.createODus(topoStructure, count)
            elif networkFunctionType == "o-ru":
                self.createORus(topoStructure, count)
            elif networkFunctionType == "ue":
                self.createUes(topoStructure, count)
            else:
                print("Unknown network function type", networkFunctionType)

    # getter
    def get(self):
        return self.topology

    # methods
    def add(self, node):
        self.topology["node"].append(node)
        return self

    def createSmos(self, topoStructure, count):
        for localId in range(count):
            config = {"node": {"localId": localId,
                               "type": "smo",
                               "function": "o-ran-common-identity-refs:smo-function"}}
            node = TapiNodeSmo(config).get()
            self.add(node)
        return self

    def createNearRtRics(self, topoStructure, count):
        return self

    def createOCus(self, topoStructure, count):
        return self

    def createODus(self, topoStructure, count):
        return self

    def createORus(self, topoStructure, count):
        return self

    def createUes(self, topoStructure, count):
        return self
