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
from typing import Dict
from lxml import etree
from model.python.tapi_node_edge_point import TapiNodeEdgePoint
from model.python.top import Top


class TapiNode(Top):
    """
    Class representing a TAPI Node.
    """

    __data: dict = {}
    __configuration: dict = {}
    __parent: 'TapiNode' = None
    __width: int = 0  # default SVG width, should be overritten by constructor

    # constructor
    def __init__(self, parent: 'TapiNode', configuration: dict):
        super().__init__(configuration)
        self.__parent = parent
        self.__configuration = configuration
        self.width((4 + 1) * (2.2*self.FONTSIZE))  # 4x nep
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
            "o-ran-sc-topology:function": configuration['node']['function'],
            "o-ran-sc-topology:geolocation": {
                "longitude": "0",
                "latitude": "0",
                "altitude": "20000"
            }
        }

    # getter
    def x_offset_by_cep_name(self, name) -> int:
        mapping: Dict[str, int] = {
            "o2-rest-consumer": -4*6*self.FONTSIZE,
            "a1-rest-consumer": -2*6*self.FONTSIZE,
            "oam-netconf-consumer": -0*6*self.FONTSIZE,
            "o1-ves-provider": 2*6*self.FONTSIZE,
            "o1-file-consumer": 4*6*self.FONTSIZE,

            "o2-rest-provider": 0*self.FONTSIZE,
            "a1-rest-provider": -3.2*self.FONTSIZE,
            "e2-rest-consumer": 0*self.FONTSIZE,

            "f1-c-unknown-consumer": 0*self.FONTSIZE,
            "f1-u-unknown-consumer": 0*self.FONTSIZE,

            "e1-unknown-provider": -5*self.FONTSIZE,
            "e1-unknown-consumer": 5*self.FONTSIZE,

            "e2-rest-provider": -4.2*self.FONTSIZE,
            "f1-c-unknown-provider": -3*self.FONTSIZE,
            "f1-u-unknown-provider": -1*self.FONTSIZE,
            "f1-unknown-provider": -2.2*self.FONTSIZE,
            "o1-netconf-provider": 2.2*self.FONTSIZE,
            "o1-ves-consumer": 1.6*self.FONTSIZE,
            "o1-file-provider": 1.6*self.FONTSIZE,
            "ofh-netconf-consumer": -1.2*self.FONTSIZE,

            "eth-ofh-provider": -1.2*self.FONTSIZE,
            "oam-netconf-provider": 1.2*self.FONTSIZE,
            "eth-ofh-consumer": 0*self.FONTSIZE,

            "ofh-netconf-provider": 0*self.FONTSIZE,
            "uu-unknown-provider": 0*self.FONTSIZE,

            "uu-unknown-consumer": 0*self.FONTSIZE
        }
        if name in mapping:
            return mapping[name]

        print("Node: CEP name", name, "for x postion calculation not found")
        return 0

    def y_offset_by_cep_name(self, name: str) -> int:
        mapping: Dict[str, int] = {
            "o2-rest-consumer": 3*self.FONTSIZE,
            "a1-rest-consumer": 3*self.FONTSIZE,
            "oam-netconf-consumer": 3*self.FONTSIZE,
            "o1-ves-provider": 3*self.FONTSIZE,
            "o1-file-consumer": 3*self.FONTSIZE,

            "o2-rest-provider": -3*self.FONTSIZE,
            "a1-rest-provider": -3*self.FONTSIZE,
            "e2-rest-consumer": 3*self.FONTSIZE,

            "e1-unknown-provider": 1*self.FONTSIZE,
            "e1-unknown-consumer": 1*self.FONTSIZE,

            "f1-c-unknown-consumer": 3*self.FONTSIZE,
            "f1-u-unknown-consumer": 3*self.FONTSIZE,
            "f1-unknown-consumer": 3*self.FONTSIZE,

            "e2-rest-provider": -3*self.FONTSIZE,
            "f1-c-unknown-provider": -3*self.FONTSIZE,
            "f1-u-unknown-provider": -3*self.FONTSIZE,
            "f1-unknown-provider": -3*self.FONTSIZE,
            "o1-netconf-provider": -3*self.FONTSIZE,
            "o1-ves-consumer": -3*self.FONTSIZE,
            "o1-file-provider": -3*self.FONTSIZE,
            "ofh-netconf-consumer": 3*self.FONTSIZE,

            "eth-ofh-provider": -3*self.FONTSIZE,
            "oam-netconf-provider": -3*self.FONTSIZE,
            "eth-ofh-consumer": +3*self.FONTSIZE,

            "ofh-netconf-provider": -3*self.FONTSIZE,
            "uu-unknown-provider": 3*self.FONTSIZE,

            "uu-unknown-consumer": -3*self.FONTSIZE
        }
        if name in mapping:
            return mapping[name]

        print("Node: CEP name", name, "for y postion calculation not found")
        return 0

    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Node configuration.
        :return TAPI Node configuration as json object.
        """
        return self.__configuration

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Link.
        :return TAPI Link as json object.
        """
        return self.__data

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
            "o-ran-sc-topology-common:smo": "SMO",
            "o-ran-sc-topology-common:o-cloud": "O-Cloud",
            "o-ran-sc-topology-common:near-rt-ric": "Near-RT-RIC",
            "o-ran-sc-topology-common:o-cu": "O-CU",
            "o-ran-sc-topology-common:o-cu-cp": "O-CU-CP",
            "o-ran-sc-topology-common:o-cu-up": "O-CU-UP",
            "o-ran-sc-topology-common:o-du": "O-DU",
            "o-ran-sc-topology-common:fronthaul-gateway": "FHGW",
            "o-ran-sc-topology-common:o-ru": "O-RU",
            "o-ran-sc-topology-common:user-equipment": "UE"
        }
        if mapping[self.function()]:
            return mapping[self.function()]
        else:
            return self.function()

    def identifier(self) -> str:
        """
        Getter returning the TAPI Node identifier.
        :return Object identifier as UUID.
        """
        return self.__data["uuid"]

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

    def node_edge_point_by_cep_name(self, cep_name) -> TapiNodeEdgePoint:
        """
        Method returning a NEP based on a given interface name
        :param interface_name: Search string
        :return The NEP uuid or "not found"
        """
        result = None
        for nep in self.__data["owned-node-edge-point"]:
            for cep in nep.connection_edge_points():
                if cep.name() == cep_name:
                    result = nep
        if result is None:
            for nep in self.__data["owned-node-edge-point"]:
                print("# Check", cep_name, nep.json()["name"][0]["value"], nep.json()["tapi-connectivity:cep-list"]["connection-end-point"][0]["name"][0]["value"])
        return result

    def parent(self) -> 'TapiNode':
        """
        Getter for a TAPI Node object representing the TAPI Node configuration.
        :return TAPI Node configuration as json object.
        """
        return self.__parent

    def svg(self, x: int, y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Node.
        :return TAPI Node as svg object.
        """
        group = etree.Element("g")
        group.attrib["class"] = "node"
        title = etree.Element("title")
        title.text = "\n TAPI Node\n id: " + \
            self.identifier() + "\n name: " + self.name()
        group.append(title)

        width = self.__width
        height = 2 * (2*self.FONTSIZE)

        rect = etree.Element("rect")
        rect.attrib["x"] = str(int(x - width/2))
        rect.attrib["y"] = str(int(y - height/2))
        rect.attrib["width"] = str(int(width))
        rect.attrib["height"] = str(int(height))
        rect.attrib["rx"] = str(self.FONTSIZE)
        rect.attrib["class"] = " ".join(["node", self.function_label().lower()])
        group.append(rect)

        label = etree.Element('text')
        label.attrib['x'] = str(x)
        # +4px for font-size 14px (think of chars like 'gjy')
        label.attrib['y'] = str(y + 4)
        label.attrib['class'] = " ".join(["node", self.function_label().lower()])
        label.text = self.function_label()
        group.append(label)

        for nep in self.data()['owned-node-edge-point']:
            nep_x = x + self.x_offset_by_cep_name(nep.connection_edge_points()[0].name())
            nep_y = y + self.y_offset_by_cep_name(nep.connection_edge_points()[0].name())
            group.append(nep.svg(nep_x, nep_y))

        return group

    def width(self, width: int) -> None:
        """
        Setter for the SVG width in px.
        :param width as integer with unit "px" (pixel)
        """
        self.__width = width

    # methods

    def add(self, nep: TapiNodeEdgePoint) -> 'TapiNode':
        """
        Method adding a TAPI Node Edge Point object.
        :return TAPI Node as object.
        """
        self.__data['owned-node-edge-point'].append(nep)
        return self
