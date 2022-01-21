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
Module for the class representing a TAPI Link
"""
import uuid
from model.python.top import Top


class TapiLink(Top):
    """
    Class representing a TAPI Link object.
    """

    __data: dict = {}
    __configuration: dict = {}

    # constructor
    def __init__(self, configuration: dict):
        self.__configuration = configuration
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "topology-link-name",
                "value": configuration['link']['name']
            }],
            "administrative-state": "LOCKED",
            "operational-state": "ENABLED",
            "direction": "BIDIRECTIONAL",
            "lifecycle-state": "INSTALLED",
            "node-edge-point": [
                configuration['link']['a'],
                configuration['link']['z']
            ],
            "latency-characteristic": [{
                "traffic-property-name": "property-1",
                "queing-latency-characteristic": "queue-1",
                "fixed-latency-characteristic": "latency-1",
                "jitter-characteristic": "jitter-1",
                "wander-characteristic": "wander-1"
            }],
            "layer-protocol-name": ["ETH"],
            "risk-characteristic": [{
                "risk-characteristic-name": "risk-name",
                "risk-identifier-list": [
                    "risk-1"]}],
            "validation-mechanism": [{
                "validation-mechanism": "mechanism-1",
                "validation-robustness": "very-robust",
                "layer-protocol-adjacency-validated": "validated"}],
            "cost-characteristic": [{
                "cost-name": "cost",
                "cost-algorithm": "alg1",
                "cost-value": "value-1"}],
            "transitioned-layer-protocol-name": ["ETH"]
        }

    # getter
    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Link.
        :return TAPI Link as json object.
        """
        return self.__data

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Link.
        :return TAPI Link as json object.
        """
        return self.data()

    def name(self) -> str:
        """
        Getter for TAPI Link name.
        :return TAPI Link as json object.
        """
        return self.__configuration['link']['name']
