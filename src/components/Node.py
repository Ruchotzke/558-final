"""
An implementation of a network node.
"""
import simpy

from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Application import Application
from src.components.stack.NetStack import NetStack
from src.components.stack.Tables import RouteEntry
from src.utilities.Logger import Logger, Level
from typing import List

# Define some types
NODE_SET = List["Node"]


class Node:
    """
    A node in a network.
    """

    nodes: NODE_SET = []
    """
    A set of all nodes in the simulation.
    """


    def __init__(self, env: simpy.Environment, name):
        self.env = env
        self.name = name
        self.stack = NetStack(env)
        Node.nodes.append(self)
        Logger.instance.log(Level.TRACE, f'Node {self.name} initialized.')

    def __del__(self):
        Node.nodes.remove(self)

    def add_interface(self, network, ether: EthernetAddr, ip: IPAddr, netm: IPAddr = IPAddr("255.255.255.0")):
        """
        Add an interface to this node.
        :param netm:
        :param ether:
        :param ip:
        :param network:
        :return:
        """
        # Add the layers
        hw_layer = self.stack.add_ethernet(ether, network)
        network.register(hw_layer)
        self.stack.add_ip(ip, hw_layer)

        # Apply the netmask
        net_addr = ip.apply_netmask(netm)
        Logger.instance.log(Level.TRACE, f"Added interface {ether}, {ip} to {self.name}")

        # Update the route table to reflect new direct entries
        entry = RouteEntry(net_addr, ip, hw_layer)
        entry.direct = True
        self.stack.route_table.insert_entry(entry)
        Logger.instance.log(Level.TRACE, f"Generated new route entry: {entry} to {self.name}")

    def install_app(self, app: Application):
        """
        Include an app on this node.
        :param app:
        :return:
        """
        self.stack.add_app(app.port, app)
        Logger.instance.log(Level.DEBUG, f"Installed {app.name} on {self.name}")