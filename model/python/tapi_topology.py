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
Module containing the main class for this project for a TAPI Topology.
"""
import uuid
from typing import Dict, List, Union
from lxml import etree

from model.python.tapi_node import TapiNode
from model.python.top import Top
from model.python.tapi_node_smo import TapiNodeSmo
from model.python.tapi_node_near_rt_ric import TapiNodeNearRtRic
from model.python.tapi_node_o_cu_cp import TapiNodeOCuCp
from model.python.tapi_node_o_cu_up import TapiNodeOCuUp
from model.python.tapi_node_o_du import TapiNodeODu
from model.python.tapi_node_o_ru import TapiNodeORu
from model.python.tapi_node_user_equipment import TapiNodeUserEquipment
from model.python.tapi_link import TapiLink


class TapiTopology(Top):
    """
    Class representing a TAPI Topology
    """

    __data: Dict[str, Union[str, List[Union[Dict, TapiNode, TapiLink]]]] = None
    __configuration: dict = None

    # constructor
    def __init__(self, configuration: dict):
        super().__init__(configuration)
        self.__configuration = configuration
        self.__data = {
            "uuid": str(uuid.uuid4()),
            "name": [{
                "value-name": "network-name",
                "value": configuration['network']['name']}],
            "layer-protocol-name": ["ETH"],
            "node": [],
            "link": []}

        topology_structure: dict = configuration['network']['pattern']
        network_function_type: str = next(iter(topology_structure))
        count: int = configuration['network']['pattern'][network_function_type]

        if network_function_type == "smo":
            self.__create_smos(None, topology_structure, count)
        elif network_function_type == "near-rt-ric":
            self.__create_near_rt_rics(None, topology_structure, count)
        elif network_function_type == "o-cu":
            self.__create_o_cus(None, topology_structure, count)
        elif network_function_type == "o-du":
            self.__create_o_dus(None, topology_structure, count)
        elif network_function_type == "o-ru":
            self.__create_o_rus(None, topology_structure, count)
        elif network_function_type == "ue":
            self.__create_ues(None, topology_structure, count)
        else:
            print("Unknown network function type", network_function_type)

    # getter
    def configuration(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology configuration.
        :return TAPI Topology configuration as json object.
        """
        return self.__configuration

    def cytoscape(self) -> Dict[str, str]:
        """
        Getter for a json object representing the TAPI Topology for topology
        representation.
        :return TAPI Topology Context as json object.
        """
        result = {}

        # nodes handling
        result["elements"] = []
        for node in self.__data["node"]:
            result["elements"].append(node.cytoscape())
            result["elements"].append({
                "group": 'nodes',
                "data": {
                    "id": "base-" + node.identifier(),
                    "parent": node.identifier(),
                    "name": "base",
                    "function": "base",
                    "hide": "true"
                }
            })
            for nep in node.data()['owned-node-edge-point']:
                result["elements"].append(nep.cytoscape())
                result["elements"].append({
                    "group": "edges",
                    "data": {
                        "id": "base-" + node.identifier() + "-" + nep.identifier(),
                        "name": "base-" + nep.name(),
                        "source": nep.identifier(),
                        "target": "base-" + node.identifier(),
                        "hide": "true",
                        "base": node.name()
                    }
                })

        # link handling
        for link in self.__data["link"]:
            result["elements"].append(link.cytoscape())

        return result

    def data(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology.
        :return TAPI Topology as json object.
        """
        return self.__data

    def identifier(self) -> str:
        """
        Getter returning the TAPI Topology identifier.
        :return Object identifier as UUID.
        """
        return self.__data["uuid"]

    def name(self) -> str:
        """
        Getter for TAPI Topology name. The TAPI topology is a representation of
        the network. Therefore, the TAPI Topology name has the same value as the
        Network name.
        :return TAPI Topology name as string.
        """
        return self.__configuration['network']['name']

    def json(self) -> dict:
        """
        Getter for a json object representing the TAPI Topology.
        :return TAPI Topology Context as json object.
        """
        result = self.data().copy()

        # nodes handling
        result["node"] = []
        for node in self.__data["node"]:
            result["node"].append(node.json())

        # link handling
        result["link"] = []
        for link in self.__data["link"]:
            result["link"].append(link.json())

        return result

    def svg(self, svg_x: int, svg_y: int) -> etree.Element:
        """
        Getter for a xml Element object representing the TAPI Topology Context.
        :return TAPI Topology Context as svg object.
        """
        group = etree.Element("g")
        desc = etree.Element("desc")
        desc.text = "\n TAPI Topology \n id: " + \
            self.identifier()  # + "\n name: " + self.name()
        group.append(desc)

        # nodes handling
        index_per_type: Dict = {}
        svg_nodes = []
        for node in self.__data["node"]:
            if type(node) in index_per_type:
                index_per_type[type(node)] = index_per_type[type(node)] + 1
            else:
                index_per_type[type(node)] = 0
            index = index_per_type[type(node)]
            node_x = svg_x + \
                index*self.__svg_dynamic_x_offset_by_node_type(type(node)) + \
                self.__svg_static_x_offset_by_node_type(type(node))
            node_y = svg_y + self.__svg_y_offset_by_node_type(type(node))
            svg_nodes.append(node.svg(node_x, node_y))
            # group.append(node.svg(node_x, node_y))

        # handling and drawing links
        for link in self.__data["link"]:
            group.append(link.svg(0, 0))

        # drawing nodes
        for svg_node in svg_nodes:
            group.append(svg_node)

        return group

    def __svg_static_x_offset_by_node_type(self, node_type) -> int:
        """
        Mapping function from node types to y position in svg
        return: int value
        """
        offset = 3*self.FONTSIZE
        pattern = self.configuration()['network']['pattern']
        x_mapping: Dict[type, int] = {
            TapiNodeSmo: 3 * self.FONTSIZE * pattern['near-rt-ric'] * pattern['o-cu'] * pattern['o-du'] * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeNearRtRic: - 3 * self.FONTSIZE + 3 * self.FONTSIZE * pattern['o-cu'] * pattern['o-du'] * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeOCuCp: - 3 * offset + 3 * self.FONTSIZE * pattern['o-du'] * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeOCuUp: + 2 * offset + 3 * self.FONTSIZE * pattern['o-du'] * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeODu: 3 * self.FONTSIZE + 2 * self.FONTSIZE * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeORu: 2 * self.FONTSIZE * pattern['user-equipment'],
            TapiNodeUserEquipment: 0
        }
        if node_type in x_mapping:
            return x_mapping[node_type]
        return 0

    def __svg_dynamic_x_offset_by_node_type(self, node_type) -> int:
        """
        Mapping function from node types to y position in svg
        return: int value
        """
        start = 0
        pattern = self.configuration()['network']['pattern']
        x_mapping: Dict[type, int] = {
            TapiNodeSmo: start + 3 * self.FONTSIZE * pattern['smo'] * pattern['near-rt-ric'] * pattern['o-cu'] * pattern['o-du'] * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeNearRtRic: start + 3 * self.FONTSIZE * pattern['near-rt-ric'] * pattern['o-cu'] * pattern['o-du'] * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeOCuCp: start + 3 * self.FONTSIZE * pattern['o-cu'] * pattern['o-du'] * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeOCuUp: start + 3 * self.FONTSIZE * pattern['o-cu'] * pattern['o-du'] * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeODu: start + 3 * self.FONTSIZE * pattern['o-du'] * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeORu: start + 3 * self.FONTSIZE * pattern['o-ru'] * pattern['user-equipment'],
            TapiNodeUserEquipment: start + 2 *
            self.FONTSIZE * pattern['user-equipment']
        }
        if node_type in x_mapping:
            return x_mapping[node_type]
        return 0

    def __svg_y_offset_by_node_type(self, node_type) -> int:
        """
        Mapping function from node types to y position in svg
        return: int value
        """
        start = 0
        offset = 140
        y_mapping: Dict[type, int] = {
            TapiNodeSmo: start + 0 * offset,
            TapiNodeNearRtRic: start + 1 * offset,
            TapiNodeOCuCp: start + 2 * offset - 20,
            TapiNodeOCuUp: start + 2 * offset + 20,
            TapiNodeODu: start + 3 * offset,
            TapiNodeORu: start + 4 * offset,
            TapiNodeUserEquipment: start + 5 * offset
        }
        if node_type in y_mapping:
            return y_mapping[node_type]
        return 0

    # methods
    def add_node(self, node: TapiNode):
        """
        Method adding a TAPI node to TAPI Topology.
        :return TAPI Topology object.
        """
        self.__data["node"].append(node)
        return self

    def add_link(self, link: TapiLink):
        """
        Method adding a TAPI node to TAPI Topology.
        :return TAPI Topology object.
        """
        self.__data["link"].append(link)
        return self

    def __create_smos(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "smo"
        next_type = "near-rt-ric"
        for local_id in range(count):
            prefix = ""

            if parent is not None:
                prefix = parent.data()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(local_id),
                               "type": current_type,
                               "function": "o-ran-common-identity-refs:"+current_type+"-function"}}
            node = TapiNodeSmo(parent, config)
            self.add_node(node)
            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_near_rt_rics(
                    node, structure, structure[next_type])
        return self

    def __create_near_rt_rics(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "near-rt-ric"
        next_type = "o-cu"
        for local_id in range(count):
            # add node
            prefix = ""
            if parent is not None:
                prefix = parent.json()["name"][1]["value"]
            function = "o-ran-common-identity-refs:"+current_type+"-function"
            node_configuration = {"node": {"localId": prefix + str(local_id),
                                           "type": current_type,
                                           "function": function}}
            node = TapiNodeNearRtRic(parent, node_configuration)
            self.add_node(node)

            # add links
            # A1
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "a1-rest",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))

            # O1 NETCONF
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "o1-netconf",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))

            # O1 FILE
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "o1-file",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))

            # O1 VES
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "o1-ves",
                "provider": parent,
                "consumer": node
            }
            self.add_link(TapiLink(link_configuration))

            # continue
            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_o_cus(node, structure, structure[next_type])

        return self

    def __function_identity(self, function_type: str, plane: str) -> str:
        """
        Method to calculate the Function IDENTITY
        """
        return "".join([
            "o-ran-common-identity-refs:",
            function_type,
            "-",
            plane,
            "-function"
        ])

    def __create_o_cus(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "o-cu"
        next_type = "o-du"
        for local_id in range(count):
            prefix = ""
            if parent is not None:
                prefix = parent.data()["name"][1]["value"]

            node: Dict[str, Union[TapiNodeOCuCp, TapiNodeOCuUp]] = {}
            for plane in ["cp", "up"]:
                config = {"node": {"localId": prefix + str(local_id),
                                   "type": "-".join([current_type, plane]),
                                   "function": self.__function_identity(current_type, plane)}}
                classes: Dict[str, Union[TapiNodeOCuCp, TapiNodeOCuUp]] = {
                    "cp": TapiNodeOCuCp,
                    "up": TapiNodeOCuUp}
                node[plane] = classes[plane](parent, config)
                self.add_node(node[plane])

                # add links
                # E2
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "e2-rest",
                    "provider": node[plane],
                    "consumer": parent
                }
                self.add_link(TapiLink(link_configuration))

                # O1 NETCONF
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-netconf",
                    "provider": node[plane],
                    "consumer": parent.parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 FILE
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-file",
                    "provider": node[plane],
                    "consumer": parent.parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 VES
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-ves",
                    "provider": parent.parent(),
                    "consumer": node[plane]
                }
                self.add_link(TapiLink(link_configuration))

            # continue
            # E1 Interface between O-CU-UP and O-CU-CP
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "e1-unknown",
                "provider": node["up"],
                "consumer": node["cp"]
            }
            self.add_link(TapiLink(link_configuration))

            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_o_dus(
                    node, structure, structure[next_type])
        return self

    def __create_o_dus(self, parents: Dict[str, TapiNode], topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "o-du"
        next_type = "o-ru"
        for local_id in range(count):
            prefix = "000"
            if parents["cp"] is not None:
                prefix = parents["cp"].data()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(local_id),
                               "type": current_type,
                               "function": "o-ran-common-identity-refs:"+current_type+"-function"}}
            node = TapiNodeODu(parents["cp"], config)
            self.add_node(node)

            for plane, parent in parents.items():

                # add links
                # E2
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "e2-rest",
                    "provider": node,
                    "consumer": parent.parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 NETCONF
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-netconf",
                    "provider": node,
                    "consumer": parent.parent().parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 FILE
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-file",
                    "provider": node,
                    "consumer": parent.parent().parent()
                }
                self.add_link(TapiLink(link_configuration))

                # O1 VES
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": "o1-ves",
                    "provider": parent.parent().parent(),
                    "consumer": node
                }
                self.add_link(TapiLink(link_configuration))

                # F1 User Plane or Control Plane
                interfaces: Dict[str, str] = {"cp": "f1-c", "up": "f1-u"}
                link_configuration = {
                    "topology_reference": self.data()["uuid"],
                    "name_prefix": interfaces[plane]+"-unknown",
                    "provider": node,
                    "consumer": parent
                }
                self.add_link(TapiLink(link_configuration))

            # continue
            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_o_rus(node, structure, structure[next_type])
        return self

    def __create_o_rus(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "o-ru"
        next_type = "user-equipment"
        for local_id in range(count):
            prefix = ""
            if parent is not None:
                prefix = parent.data()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(local_id),
                               "type": current_type,
                               "function": "o-ran-common-identity-refs:"+current_type+"-function"}}
            node = TapiNodeORu(parent, config)
            self.add_node(node)

            # add links

            # O1 NETCONF
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "ofh-netconf",
                "provider": node,
                "consumer": parent.parent().parent().parent()
            }
            self.add_link(TapiLink(link_configuration))

            # OFH M-Plane to O-DU
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "ofh-netconf",
                "provider": node,
                "consumer": parent
            }
            self.add_link(TapiLink(link_configuration))

            # continue
            if next_type in topology_structure:
                structure = topology_structure.copy()
                if current_type in structure:
                    del structure[current_type]
                self.__create_ues(node, structure, structure[next_type])
        return self

    def __create_ues(self, parent: TapiNode, topology_structure: dict, count: int):
        """
        Method adding a TAPI node to TAPI Topology.
        :param parent: A TAPI node which acts a a parent node in the topology.
        :param topology_structure: Information about the next topology levels.
        :param count: Number of instance to be created
        :return TAPI Topology object.
        """
        current_type = "user-equipment"
        for local_id in range(count):
            prefix = ""
            if parent is not None:
                prefix = parent.data()["name"][1]["value"]
            config = {"node": {"localId": prefix + str(local_id),
                               "type": current_type,
                               "function": "o-ran-common-identity-refs:"+current_type+"-function"}}
            node = TapiNodeUserEquipment(parent, config)
            self.add_node(node)

            # add links
            # Uu unknown
            link_configuration = {
                "topology_reference": self.data()["uuid"],
                "name_prefix": "uu-unknown",
                "provider": parent,
                "consumer": node
            }
            self.add_link(TapiLink(link_configuration))

            if "key" in topology_structure:
                print("Implement missing topology level.")

        return self
