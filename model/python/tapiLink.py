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


class TapiLink:

    link = {}
    config = {}

    # constructor
    def __init__(self, config):
        self.config = config
        self.link = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "topology-link-name",
                "value": self.getLinkName(config['link'])
            }],
            "administrative-state": "LOCKED",
            "operational-state": "ENABLED",
            "direction": "BIDIRECTIONAL",
            "lifecycle-state": "INSTALLED",
            "node-edge-point": [{
                "topology-uuid": self.getTopologyIdByNepId(config['link']['a']),
                "node-uuid": self.getNodeIdByNepId(config['link']['a']),
                "node-edge-point-uuid": config['link']['a']
            }, {
                "topology-uuid": self.getTopologyIdByNepId(config['link']['z']),
                "node-uuid": self.getNodeIdByNepId(config['link']['z']),
                "node-edge-point-uuid": config['link']['z']
            }],
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
            "transitioned-layer-protocol-name": [
                "layer-protocol-2---should-it-be-an-uuid?",
                "layer-protocol-1---should-it-be-an-uuid?"]
        }

    # getter
    def get(self):
        return self.link

    def getLinkName(self, link):
        return "TODO"

    def getNodeIdByNepId(self, nepUuid):
        return "TODO"

    def getTopologyIdByNepId(self, nepUuid):
        return "TODO"
