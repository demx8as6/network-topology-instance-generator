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
from model.python.tapiNode import TapiNode
from model.python.tapiNodeEdgePoint import TapiNodeEdgePoint


class TapiNodeSmo(TapiNode):

    # constructor
    def __init__(self, parent, config):
        super().__init__(parent, config)
        # add A1 consumer interface
        a1ConsumerConfig = {"nodeEdgePoint": {
            "interface": "a1",  "protocol": "REST", "role": "consumer"}}
        a1Consumer = TapiNodeEdgePoint(a1ConsumerConfig)
        self.add(a1Consumer)

        # add O1/OAM NetConf Consumer interface
        o1NcConsumerConfig = {"nodeEdgePoint": {
            "interface": "o1", "protocol": "NETCONF", "role": "consumer"}}
        o1NcConsumer = TapiNodeEdgePoint(o1NcConsumerConfig)
        self.add(o1NcConsumer)

        # add O1 VES Provider interface
        o1VesProviderConfig = {"nodeEdgePoint": {
            "interface": "o1", "protocol": "VES", "role": "provider"}}
        o1VesProvider = TapiNodeEdgePoint(o1VesProviderConfig)
        self.add(o1VesProvider)

        # add O1 File Transfer Consumer interface
        o1FileConsumerConfig = {"nodeEdgePoint": {
            "interface": "o1", "protocol": "FILE", "role": "consumer"}}
        o1FileConsumer = TapiNodeEdgePoint(o1FileConsumerConfig)
        self.add(o1FileConsumer)
