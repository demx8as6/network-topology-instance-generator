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
import sys

from controller.parameterValidator import ParameterValidator
from controller.networkGenerator import TopologyGenerator
from view.networkViewer import NetworkViewer

validator = ParameterValidator(sys.argv)

if validator.isValid():
  config = validator.getConfiguration()
  generator = TopologyGenerator(config)
  generator.generate()
  print('   configFile:', validator.getConfigFile())
  print('configuration:', generator.getConfiguration())

  viewer = NetworkViewer(generator.getTopology())

  filename = "output/network.json"
  if config['network']['name']:
    filename = "output/" + config['network']['name'] + ".json"
  viewer.json().save(filename)
  viewer.json().show()

else:
  print(validator.getError())