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


class TapiNodeNearRtRic(TapiNode):

    # constructor
    def __init__(self, parent, config):
        super().__init__(parent, config)
        # add A1 provider interface
        a1ProviderConfig = {"nodeEdgePoint": {
            "interface": "a1",  "protocol": "REST", "role": "provider"}}
        a1Provider = TapiNodeEdgePoint(a1ProviderConfig).get()
        self.add(a1Provider)

        # add E2 Consumer interface
        e2ConsumerConfig = {"nodeEdgePoint": {
            "interface": "e2", "protocol": "REST", "role": "consumer"}}
        e2Consumer = TapiNodeEdgePoint(e2ConsumerConfig).get()
        self.add(e2Consumer)

        # add O1/OAM NetConf Provider interface
        o1NcProviderConfig = {"nodeEdgePoint": {
            "interface": "o1", "protocol": "NETCONF", "role": "Provider"}}
        o1NcProvider = TapiNodeEdgePoint(o1NcProviderConfig).get()
        self.add(o1NcProvider)

        # add O1 VES Consumer interface
        o1VesConsumerConfig = {"nodeEdgePoint": {
            "interface": "o1", "protocol": "VES", "role": "consumer"}}
        o1VesConsumer = TapiNodeEdgePoint(o1VesConsumerConfig).get()
        self.add(o1VesConsumer)

        # add O1 File Transfer Provider interface
        o1FileProviderConfig = {"nodeEdgePoint": {
            "interface": "o1", "protocol": "FILE", "role": "provider"}}
        o1FileProvider = TapiNodeEdgePoint(o1FileProviderConfig).get()
        self.add(o1FileProvider)
