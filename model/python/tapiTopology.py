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
from model.python.top import Top
from model.python.tapiNodeSmo import TapiNodeSmo
from model.python.tapiNodeNearRtRic import TapiNodeNearRtRic
from model.python.tapiNodeOCu import TapiNodeOCu
from model.python.tapiNodeODu import TapiNodeODu
from model.python.tapiNodeORu import TapiNodeORu
from model.python.tapiNodeUserEquipment import TapiNodeUserEquipment
from model.python.tapiLink import TapiLink

class TapiTopology(Top):

    data = {}

    # constructor
    def __init__(self, config):
        self.data = {
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
    def getData(self):
        return self.data

    # methods
    def addNode(self, node):
        self.data["node"].append(node)
        return self

    def addLink(self, link):
        self.data["link"].append(link)
        return self

    def toJson(self):
        result = self.getData().copy()

        # nodes handling
        result["node"] = []
        for node in self.data["node"]:
            result["node"].append(node.toJson())

        # link handling 
        result["link"] = []
        for link in self.data["link"]:
            result["link"].append(link.toJson())

        return result

    def createSmos(self, parent, topoStructure, count):
        currentType = "smo"
        nextType = "near-rt-ric"
        for localId in range(count):
            prefix = ""

            if parent != None:
                prefix = parent.getData()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeSmo(parent, config)
            self.addNode(node)
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
            # add node
            prefix = ""
            if parent != None:
                prefix = parent.getData()["name"][1]["value"]
            nodeConfig = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeNearRtRic(parent, nodeConfig)
            self.addNode(node)
            
            # add links
            a1LinkConfig = {"link":{
                "name": "A1:|" + parent.getName() + "|<->|" + node.getName() + "|",
                "a":{
                    "topology-uuid":self.data["uuid"],
                    "node-uuid": parent.getData()["uuid"],
                    "node-edge-point-uuid": parent.getNodeEdgePointByInterfaceName("a1-rest-consumer")
                },
                "z":{
                    "topology-uuid":self.data["uuid"],
                    "node-uuid": node.getData()["uuid"],
                    "node-edge-point-uuid": node.getNodeEdgePointByInterfaceName("a1-rest-provider")
                }
            }}
            a1Link =  TapiLink(a1LinkConfig)
            self.addLink(a1Link)

            # continue
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
                prefix = parent.getData()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeOCu(parent, config)
            self.addNode(node)
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
                prefix = parent.getData()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeODu(parent, config)
            self.addNode(node)
            if nextType in topoStructure:
                structure = topoStructure.copy()
                if currentType in structure:
                    del structure[currentType]
                self.createORus(node, structure, structure[nextType])
        return self

    def createORus(self, parent, topoStructure, count):
        currentType = "o-ru"
        nextType = "user-equipment"
        for localId in range(count):
            prefix = ""
            if parent != None:
                prefix = parent.getData()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeORu(parent, config)
            self.addNode(node)
            if nextType in topoStructure:
                structure = topoStructure.copy()
                if currentType in structure:
                    del structure[currentType]
                self.createUes(node, structure, structure[nextType])
        return self

    def createUes(self, parent, topoStructure, count):
        currentType = "user-equipment"
        for localId in range(count):
            prefix = ""
            if parent != None:
                prefix = parent.getData()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(localId),
                               "type": currentType,
                               "function": "o-ran-common-identity-refs:"+currentType+"-function"}}
            node = TapiNodeUserEquipment(parent, config)
            self.addNode(node)
        return self
