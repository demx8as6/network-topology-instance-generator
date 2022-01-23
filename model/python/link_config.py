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
Module to construct the input configuration for a TAPI link object.
"""
from typing import Dict
from model.python.tapi_node import TapiNode
from model.python.top import Top


class LinkConfig(Top):
    """
    Class containing  methods creating an link configuration object.
    """

    __topology_reference = "unknown"
    __name_prefix: str = "unknown"
    __consumer: TapiNode = None
    __provider: TapiNode = None

    __data: dict = {"link": {
        "name": "noName",
        "a": {},
        "z": {}
    }}

    # constructor
    def __init__(self, topology_reference: str, name_prefix: str,
                 provider: TapiNode, consumer: TapiNode):
        super().__init__({})
        self.__topology_reference = topology_reference
        self.__name_prefix = name_prefix
        self.__consumer = consumer
        self.__provider = provider

        # exception for O-RAN Fronthaul Management plane to SMO
        consumer_name_prefix = name_prefix
        if consumer_name_prefix == "open-fronthaul-m-plane-netconf":
            consumer_name_prefix = "o1-netconf"

        self.data = {"link": {
            "name": self.name(),
            "a": {
                "topology-uuid": topology_reference,
                "node-uuid": consumer.data()["uuid"],
                "node-edge-point-uuid":
                    consumer.node_edge_point_by_interface_name(
                        consumer_name_prefix.lower() + "-consumer")
            },
            "z": {
                "topology-uuid": topology_reference,
                "node-uuid": provider.data()["uuid"],
                "node-edge-point-uuid":
                    provider.node_edge_point_by_interface_name(
                        name_prefix.lower() + "-provider")
            }
        }}

    def configuration(self) -> Dict[str, Dict[str, Dict]]:
        """
        Getter returning the configuration.
        :return Link identifier as string
        """
        return {"configuration": {
            "topology-reference:": self.__topology_reference,
            "name_prefix": self.__name_prefix,
            "provider": self.__provider.json(),
            "consumer": self.__consumer.json()
        }}

    def data(self) -> Dict[str, Dict]:
        """
        Getter returning the link configuration identifier of the link.
        :return Link identifier as string
        """
        return self.__data

    def identifier(self) -> str:
        """
        Getter returning the link configuration identifier of the link.
        :return Link identifier as string
        """
        return "--".join([
            self.__consumer.identifier(),
            self.__provider.identifier(),
        ])

    def name(self) -> str:
        """
        Getter returning the name of the link.
        :return Link name as string
        """
        return "|".join([
            self.__name_prefix.upper(),
            self.__consumer.name(),
            "->",
            self.__provider.name(), ""
        ])

    def json(self) -> dict:
        """
        Getter for the json represention of this object.
        :return JSON object of link configuration
        """
        return self.data
