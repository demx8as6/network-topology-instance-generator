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
"""
Module containing the class for a TAPI Node.
"""
import uuid
from model.python.tapi_node_edge_point import TapiNodeEdgePoint
from model.python.top import Top

class TapiNode(Top):
    """
    Class representing a TAPI Node.
    """

    __data: dict = {}
    __configuration: dict = {}
    __parent: 'TapiNode' = None

    # constructor
    def __init__(self, parent: 'TapiNode', configuration: dict):
        super().__init__(configuration)
        self.__parent = parent
        self.__configuration = configuration
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [
                {
                    "value-name": "topology-node-name",
                    "value": self.name()
                },
                {
                    "value-name": "topology-node-local-id",
                    "value": configuration['node']['localId']
                }
            ],
            "owned-node-edge-point": [],
            "administrative-state": "LOCKED",
            "operational-state": "ENABLED",
            "lifecycle-state": "INSTALLED",
            "layer-protocol-name": ["ETH"],
            "cost-characteristic": [
                {
                    "cost-name": "cost",
                    "cost-algorithm": "alg1",
                    "cost-value": "value-1"
                }
            ],
            "latency-characteristic": [{
                "traffic-property-name": "property-1",
                "queing-latency-characteristic": "queue-1",
                "fixed-latency-characteristic": "latency-1",
                "jitter-characteristic": "jitter-1",
                "wander-characteristic": "wander-1"
            }],
            "o-ran-topology:function": configuration['node']['function'],
            "o-ran-topology:geolocation": {
                "longitude": "0",
                "latitude": "0",
                "altitude": "20000"
            }
        }

    # getter
    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Node configuration.
        :return TAPI Node configuration as json object.
        """
        return self.__configuration

    def parent(self) -> 'TapiNode':
        """
        Getter for a TAPI Node object representing the TAPI Node configuration.
        :return TAPI Node configuration as json object.
        """
        return self.__parent

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Link.
        :return TAPI Link as json object.
        """
        return self.__data

    def identifier(self) -> str:
        """
        Getter returning the TAPI Node identifier.
        :return Object identifier as UUID.
        """
        return self.__data["uuid"]

    def name(self) -> str:
        """
        Getter for TAPI Node name.
        :return TAPI Node as json object.
        """
        return "".join([
            self.__configuration['node']['type'],
            "-",
            str(self.__configuration['node']['localId'])
        ])

    def node_edge_point_by_interface_name(self, interface_name) -> str:
        """
        Method returning a NEP based on a given interface name
        :param interface_name: Search string
        :return The NEP uuid or "not found"
        """
        result = "not found"
        for nep in self.__data["owned-node-edge-point"]:
            if nep.name() == interface_name:
                result = nep.data()["uuid"]
        if result == "not found":
            print(interface_name, result)
            for nep in self.__data["owned-node-edge-point"]:
                print(nep.json())
        return result

    def function(self) -> str:
        """
        Getter returning the network-function type
        :return The type of the network-function as yang IDENTITY.
        """
        return self.__configuration['node']['function']

    def function_label(self) -> str:
        """
        Getter returning the network-function label
        :return The type of the network-function as human readable string.
        """
        mapping = {
            "o-ran-common-identity-refs:smo-function": "SMO",
            "o-ran-common-identity-refs:near-rt-ric-function": "Near-RT-RIC",
            "o-ran-common-identity-refs:o-cu-function": "O-CU",
            "o-ran-common-identity-refs:o-cu-cp-function": "O-CU-CP",
            "o-ran-common-identity-refs:o-cu-up-function": "O-CU-UP",
            "o-ran-common-identity-refs:o-du-function": "O-DU",
            "o-ran-common-identity-refs:o-ru-function": "O-RU",
            "o-ran-common-identity-refs:user-equipment-function": "UE"
        }
        if mapping[self.function()]:
            return mapping[self.function()]
        else:
            return self.function()

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Node.
        :return TAPI Node as json object.
        """
        result = self.__data.copy()
        result['owned-node-edge-point'] = []
        for nep in self.__data['owned-node-edge-point']:
            result['owned-node-edge-point'].append(nep.json())
        return result

    # methods
    def add(self, nep: TapiNodeEdgePoint) -> 'TapiNode':
        """
        Method adding a TAPI Node Edge Point object.
        :return TAPI Node as object.
        """
        self.__data['owned-node-edge-point'].append(nep)
        return self
