#!/usr/bin/python

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
Module for a class representing a TAPI Common Context
"""
from typing import Dict, Union
import uuid
from model.python.tapi_topology_context import TapiTopologyContext
from model.python.top import Top


class TapiCommonContext(Top):
    """
    Class representing a TAPI Common Context object.
    """

    __configuration: dict = {}
    __context: TapiTopologyContext = None
    __data: dict = {
        "tapi-common:context": {
            "uuid": str(uuid.uuid4()),
            "name": [{"value-name": "context-name",
                      "value": "Generated Topology"}]}}

    # constructor
    def __init__(self, configuration: Dict[str, Union[str, Dict[str, int]]]):
        super().__init__(configuration)
        self.__context = TapiTopologyContext(configuration)

    # getter
    def configuration(self) -> Dict[str, Dict]:
        """
        Getter for a json object representing the TAPI Common Context.
        :return TAPI Common Context as json object.
        """
        return self.__configuration

    def cytoscape(self) -> Dict[str, str]:
        """
        Getter returning the object for topology visualization.
        :return Cytoscape root.
        """
        result = {
            "layout": {"name": "grid"},
            "style": [
                {
                    "selector": "node",
                    "style": {
                        "background-color": "#2B65EC"
                    }
                },
                {
                    "selector": ":parent",
                    "style": {
                        "background-opacity": 0.333,
                        "border-color": "#2B65EC"
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#2B65EC"
                    }
                },
                {
                    "selector": "node:selected",
                    "style": {
                        "background-color": "#F08080",
                        "border-color": "red"
                    }
                },
                {
                    "selector": "edge:selected",
                    "style": {
                        "line-color": "#F08080"
                    }
                }
            ],
            "elements": []
        }
        result.update(self.__context.cytoscape())
        return result

    def data(self) -> Dict:
        """
        Getter for a json object representing the TAPI Common Context.
        :return TAPI Common Context as json object.
        """
        return self.__data

    def json(self) -> Dict:
        """
        Getter for a json object representing the TAPI Topology Context.
        :return TAPI Common Context as json object.
        """
        result = self.data().copy()
        if self.__context is not None:
            result["tapi-common:context"].update(self.__context.json())

        return result

    def identifier(self) -> str:
        """
        Getter returning the TAPI common context identifier.
        :return Object identifier as string
        """
        return self.__data["tapi-common:context"]["uuid"]

    def name(self) -> str:
        """
        Getter for object name.
        :return Human readable string as name.
        """
        return self.data()["tapi-common:context"]["name"][0]["value"]

    def topology_context(self) -> TapiTopologyContext:
        """
        Getter for next level object (TapiTopologyContext).
        :return TAPI Topology Context
        """
        return self.__context
