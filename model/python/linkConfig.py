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
from model.python.top import Top


class LinkConfig(Top):

    consumer = None
    provider = None
    topoRef = "unknown"
    namePrefix = "unknown"

    data = {"link": {
        "name": "noName",
        "a": {},
        "z": {}
    }}

    # constructor
    def __init__(self, topoRef, namePrefix, provider, consumer):
        self.consumer = consumer
        self.provider = provider
        self.topoRef = topoRef
        self.namePrefix = namePrefix

        # execption for O-RAN Fronthaul Management plane to SMO
        consumerNamePrefix = namePrefix 
        if consumerNamePrefix == "open-fronthaul-m-plane-netconf":
          consumerNamePrefix = "o1-netconf"

        self.data = {"link": {
            "name": self.getName(),
            "a": {
                "topology-uuid": topoRef,
                "node-uuid": consumer.getData()["uuid"],
                "node-edge-point-uuid": consumer.getNodeEdgePointByInterfaceName(consumerNamePrefix.lower() + "-consumer")
            },
            "z": {
                "topology-uuid": topoRef,
                "node-uuid": provider.getData()["uuid"],
                "node-edge-point-uuid": provider.getNodeEdgePointByInterfaceName(namePrefix.lower() + "-provider")
            }
        }}

    def getName(self):
        return self.namePrefix.upper() + "|" + self.consumer.getName() + "|->|" + self.provider.getName() + "|"

    def toJson(self):
        return self.data