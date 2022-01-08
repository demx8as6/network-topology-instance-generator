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
from model.python.tapiNodeNearRtRic import TapiNodeNearRtRic
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
        networkFunctionType = next(iter(topoStructure))
        count = config['network']['pattern'][networkFunctionType]

        if networkFunctionType == "smo":
            self.createSmos(None, topoStructure, count)
        elif networkFunctionType == "near-rt-ric":
            self.createNearRtRics(None, topoStructure, count)
        elif networkFunctionType == "o-cu":
            self.createOCus(None, topoStructure, count)
        elif networkFunctionType == "o-du":
            self.createODus(None, topoStructure, count)
        elif networkFunctionType == "o-ru":
            self.createORus(None, topoStructure, count)
        elif networkFunctionType == "ue":
            self.createUes(None, topoStructure, count)
        else:
            print("Unknown network function type", networkFunctionType)

    # getter
    def get(self):
        return self.topology

    # methods
    def add(self, node):
        self.topology["node"].append(node)
        return self

    def createSmos(self, parent, topoStructure, count):
        currentType = "smo"
        nextType = "near-rt-ric"
        for localId in range(count):
            prefix = ""
            if parent != None:
                prefix = parent["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeSmo(config).get()
            self.add(node)
            if nextType in topoStructure:
                structure = topoStructure.copy()
                if currentType in structure:
                    del structure[currentType]
                self.createNearRtRics(node, structure, structure[nextType])
        return self

    def createNearRtRics(self, parent, topoStructure, count):
        currentType = "near-rt-ric"
        nextType = "o-cu"
        for localId in range(count):
            prefix = ""
            if parent != None:
                prefix = parent["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeNearRtRic(config).get()
            self.add(node)
            if nextType in topoStructure:
                structure = topoStructure.copy()
                if currentType in structure:
                    del structure[currentType]
                self.createOCus(node, structure, structure[nextType])
        return self

    def createOCus(self, parent, topoStructure, count):
        currentType = "o-cu"
        nextType = "o-du"
        for localId in range(count):
            prefix = ""
            if parent != None:
                prefix = parent["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeNearRtRic(config).get()
            self.add(node)
            if nextType in topoStructure:
                structure = topoStructure.copy()
                if currentType in structure:
                    del structure[currentType]
                self.createODus(node, structure, structure[nextType])
        return self

    def createODus(self, parent, topoStructure, count):
        currentType = "o-du"
        nextType = "o-ru"
        for localId in range(count):
            prefix = ""
            if parent != None:
                prefix = parent["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeNearRtRic(config).get()
            self.add(node)
            if nextType in topoStructure:
                structure = topoStructure.copy()
                if currentType in structure:
                    del structure[currentType]
                self.createORus(node, structure, structure[nextType])
        return self

    def createORus(self, parent, topoStructure, count):
        currentType = "o-ru"
        nextType = "ue"
        for localId in range(count):
            prefix = ""
            if parent != None:
                prefix = parent["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeNearRtRic(config).get()
            self.add(node)
            if nextType in topoStructure:
                structure = topoStructure.copy()
                if currentType in structure:
                    del structure[currentType]
                self.createUes(node, structure, structure[nextType])
        return self

    def createUes(self, parent, topoStructure, count):
        print("### UE?", count)
        return self
