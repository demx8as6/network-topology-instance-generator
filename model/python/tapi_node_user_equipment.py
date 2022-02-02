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
Module containing a class representing a User Equipment as TAPI Node.
"""
from model.python.svg_rounded_rect import RoundedRectangel
from model.python.tapi_node import TapiNode
from model.python.tapi_node_edge_point import TapiNodeEdgePoint
from lxml import etree


class TapiNodeUserEquipment(TapiNode):
    """
    Class representing a User Equipment as TAPI Node
    """

    __nep_x_offset = 0
    __nep_y_offest = 0

    # constructor
    def __init__(self, parent, config):
        super().__init__(parent, config)

        self.__nep_x_offset = 0
        self.__nep_y_offest = -2*self.FONTSIZE

        # add air consumer interface
        nep_configuration = {
            "parent": self.identifier(),
            "nodeEdgePoint": {
                "interface": "uu", "protocol": "unknown", "role": "consumer"
            }
        }
        self.add(TapiNodeEdgePoint(nep_configuration))

    def svg(self, x: int, y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Node.
        :return TAPI Node as svg object.
        """
        group = etree.Element("g")
        desc = etree.Element("desc")
        desc.text = "\n TAPI Node User Equipment\n id: " + \
            self.identifier() + "\n name: " + self.name()
        group.append(desc)

        width = 1 * (2*self.FONTSIZE) + 1*(2*self.FONTSIZE)
        height = 2 * (2*self.FONTSIZE)
        rect = RoundedRectangel(
            {'x': x, 'y': y, 'width': width, 'height': height, 'radius': super().FONTSIZE})
        group.append(rect.svg())

        label = etree.Element('text')
        label.attrib['x'] = str(x)
        # +4px for font-size 14px (think of chars like 'gjy')
        label.attrib['y'] = str(y + 4)
        label.text = self.function_label()
        group.append(label)

        index = 0
        for nep in super().data()['owned-node-edge-point']:
            nep_x = x + (self.__nep_x_offset * index)
            nep_y = y + self.__nep_y_offest
            group.append(nep.svg(nep_x, nep_y))
            index = index + 1

        return group
