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


class TapiNodeOCu(TapiNode):

    # constructor
    def __init__(self, parent, config):
        super().__init__(parent, config)

        # add E2 Provider interface
        e2ProviderConfig = {"nodeEdgePoint": {
            "interface": "e2", "protocol": "REST", "role": "provider"}}
        e2Provider = TapiNodeEdgePoint(e2ProviderConfig)
        self.add(e2Provider)

        # add O1/OAM NetConf Provider interface
        o1NcProviderConfig = {"nodeEdgePoint": {
            "interface": "o1", "protocol": "NETCONF", "role": "provider"}}
        o1NcProvider = TapiNodeEdgePoint(o1NcProviderConfig)
        self.add(o1NcProvider)

        # add O1 VES Consumer interface
        o1VesConsumerConfig = {"nodeEdgePoint": {
            "interface": "o1", "protocol": "VES", "role": "consumer"}}
        o1VesConsumer = TapiNodeEdgePoint(o1VesConsumerConfig)
        self.add(o1VesConsumer)

        # add O1 File Transfer Provider interface
        o1FileProviderConfig = {"nodeEdgePoint": {
            "interface": "o1", "protocol": "FILE", "role": "provider"}}
        o1FileProvider = TapiNodeEdgePoint(o1FileProviderConfig)
        self.add(o1FileProvider)
