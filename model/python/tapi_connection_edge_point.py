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
Module containing a class representing a TAPI Connection Node Edge Point
"""
import uuid
from typing import Dict, Union
from lxml import etree
from model.python.top import Top


class TapiConnectionEdgePoint(Top):
    """
    Class representing a TAPI Connection Node Edge Point object
    """

    __data: Dict = {}
    __configuration = {
        "protocol": "unknown",
        "role": "consumer",
        "parent": {
            "node": "unknown",
            "node-edge-point": "unknown",
            "interface": "unknown"
        }
    }

    # constructor
    def __init__(self, configuration: Dict[str, str]):
        super().__init__(configuration)
        self.__configuration = configuration
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "connection-edge-point-name",
                "value": self.name()
            }],
            "operational-state": "ENABLED",
            "lifecycle-state": "INSTALLED",
            "termination-state": self.termination_state(),
            "termination-direction": self.termination_direction(),
            "layer-protocol-name": "ETH",
            "layer-protocol-qualifier": self.protocol(),

            "connection-port-role": "SYMMETRIC",
            "connection-port-direction": "BIDIRECTIONAL",

            "parent-node-edge-point": {
                #  TODO              "topology-uuid": "?",
                "node-uuid": self.parent()["node"],
                "node-edge-point-uuid": self.parent()["node-edge-point"]
            }
        }

    # getter
    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Node Edge Point intiail
        configuration.
        :return TAPI Node Edge Point configuration as json object.
        """
        return self.__configuration

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Node Edge Point.
        :return TAPI Node Edge Point as json object.
        """
        return self.__data

    def identifier(self) -> str:
        """
        Getter returning the TAPI Node Edge Point identifier.
        :return Object identifier as UUID.
        """
        return self.__data["uuid"]

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Node Edge Point.
        :return TAPI Node Edge Point as json object.
        """
        return self.data()

    def name(self) -> str:
        """
        Getter a human readable identifier of the TAPI Node Edge Point.
        :return TAPI Node Edge Point name as String.
        """
        items = (self.parent()["interface"],
                 self.protocol().split(":")[1],
                 self.role())
        return "-".join(items).lower()

    def __label_by_protocol(self, protocol) -> str:
        mapping: Dict[str, str] = {
            "netconf": "NC",
            "ves": "VES",
            "file": "FTP",
            "ofh":"OFH",
            "rest":"REST",
            "restconf":"RC",
            "unknown":"-"
        }
        search = protocol.split(":")[1]
        if search in mapping:
            return mapping[search]
        return self.protocol()

    def protocol(self) -> str:
        """
        Getter a human readable identifier of the TAPI Connection Edge Point protocol.
        :return protocol label.
        """
        return ":".join(["o-ran-sc-topology-common", self.__configuration['protocol'].lower()])

    def role(self) -> str:
        """
        Getter a human readable identifier of the TAPI Node Edge Point role.
        :return role label.
        """
        return self.__configuration['role'].lower()

    def parent(self) -> Dict:
        """
        Getter returning the identifier the the TAPI Node hosting the Node
        Edge Point.
        :return Identifier of the TAPI Node containing this NEP.
        """
        return self.__configuration["parent"]

    def svg_x(self) -> int:
        return self.__svg_x

    def svg_y(self) -> int:
        return self.__svg_y

    def svg(self, x: int, y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Node Edge Point.
        :return TAPI Node Edge Point as SVG object.
        """
        self.__svg_x = x
        self.__svg_y = y
        group = etree.Element("g")
        group.attrib["class"] = "cep"
        title = etree.Element("title")
        title.text = "\n TAPI Connection Edge Point \n id: " + \
            self.identifier() + "\n name: " + self.name()
        group.append(title)

        circle = etree.Element("circle")
        circle.attrib['cx'] = str(x)
        circle.attrib['cy'] = str(y)
        circle.attrib['r'] = str(super().FONTSIZE)
        circle.attrib['class'] = " ".join(["cep", self.role()])

        group.append(circle)

        label = etree.Element('text')
        label.attrib['x'] = str(x)
        # +4px for font-size 14px (think of chars like 'gjy')
        label.attrib['y'] = str(y + 4)
        label.text = self.__label_by_protocol(self.protocol())
        group.append(label)

        return group

    def termination_direction(self) -> str:
        """
        Getter returning the TAPI Node Edge Point direction.
        :return TAPI Node Edge Point direction as String.
        """
        mapping = {
            "consumer": "SINK",
            "provider": "SOURCE"
        }
        if self.__configuration['role'].lower() in mapping:
            return mapping[self.__configuration['role'].lower()]
        return "BIDIRECTIONAL"

    def termination_state(self) -> str:
        """
        Getter returning the TAPI Node Edge Point state.
        :return TAPI Node Edge Point state as String.
        """
        return "LT_PERMENANTLY_TERMINATED"
