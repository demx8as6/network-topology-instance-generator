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
Module containing a class for a SVG object representing a rounded rectangle.
"""
from typing import Dict
from lxml import etree


class RoundedRectangel():
    """
    Class representing a rounded rectangle
    """

    __x = 0
    __y = 0
    __width = 100
    __height = 100
    __radius = 10
    __function = ""

    # constructor
    def __init__(self, configuration: Dict[str, int]):
        self.__x = configuration['x']
        self.__y = configuration['y']
        self.__width = configuration['width']
        self.__height = configuration['height']
        self.__radius = configuration['radius']
        self. __function  = configuration['function']

    def svg(self) -> etree.Element:
        """
        Getter for a SVG Object representing a the object.
        :return SVG Element
        """
        W = str(self.__width - 2 * self.__radius)
        H = str(self.__height - 2 * self.__radius)
        X = str(self.__x)
        # this is correct due to the starting point of the path
        Y = str(self.__y)
        R = str(self.__radius)
        # <path d="
        # M100,100
        # h200
        # a20,20 0 0 1 20,20
        # v200
        # a20,20 0 0 1 -20,20
        # h-200
        # a20,20 0 0 1 -20,-20
        # v-200
        # a20,20 0 0 1 20,-20
        # z" />
        path = etree.Element("path")
        path.attrib['d'] = "M" + X + "," + Y + " " + \
            "m-" + str(int(W)/2) + ",-" + str(self.__height/2) + " " + \
            "h" + W + " " + \
            "a" + R + "," + R + " 0 0 1 " + R + "," + R + " " + \
            "v" + H + " " + \
            "a" + R + "," + R + " 0 0 1 -" + R + "," + R + " " + \
            "h-" + W + " " + \
            "a" + R + "," + R + " 0 0 1 -" + R + ",-" + R + " " + \
            "v-" + H + " " + \
            "a" + R + "," + R + " 0 0 1 " + R + ",-" + R + " " + \
            "z"
        path.attrib["class"] = " ".join(["node", self.__function])
        return path
