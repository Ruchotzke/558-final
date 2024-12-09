"""
A simple implementation of a network stack.
"""
import simpy

from src.components.Network import Network
from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Ethernet import EthernetLayer
from src.components.stack.IP import IPLayer
from src.components.stack.Tables import RouteTable, ArpTable
from src.utilities.Logger import Logger, Level
from typing import Dict

# Some types
ETHER_LAYERS = Dict[Network, EthernetLayer]
IP_LAYERS = Dict[EthernetLayer, IPLayer]

class NetStack:
    """
    A collection of processes representing a host's network stack.
    """

    def __init__(self, env: simpy.Environment):
        self.env = env
        self.ethers: ETHER_LAYERS = {}    # Map of networks to ethernet layers
        self.ips: IP_LAYERS = {}       # Map of ethernet layers to IP layers
        self.apps = []
        self.route_table = RouteTable() # Route Table
        self.arp_table = ArpTable()     # ARP Cache

    def add_ethernet(self, ether: EthernetAddr, net):
        """
        Add a new Ethernet layer to this stack.
        :param net:
        :param ether:
        :return:
        """
        # Generate a new layer
        layer = EthernetLayer(self.env, ether, self)
        self.ethers[net] = layer
        return layer

    def add_ip(self, ip: IPAddr, ether_layer: EthernetLayer):
        """
        Add a new IP layer to this stack.
        :param ip:
        :param ether_layer:
        :return:
        """
        # Generate a new layer
        layer = IPLayer(self.env, ip, self)
        self.ips[ether_layer] = layer
        return layer

    def set_router(self, should_route: bool):
        """
        Configure this device as a router or not
        :param should_route:
        :return:
        """
        for ip in self.ips.values():
            Logger.instance.log(Level.TRACE, f"Reconfiguring {ip.addr} as router.")
            ip.router = should_route


    def get_ip_for_ether(self, ether: EthernetAddr):
        """
        Find the corresponding IP address for an Ethernet address
        :param ether:
        :return:
        """
        for layer in self.ips.keys():
            if layer.addr == ether:
                return self.ips[layer]
        Logger.instance.log(Level.ERROR, f"Unable to map {ether} to an IP address within stack.")
        return None

    def get_network(self, layer: EthernetLayer):
        for net in self.ethers.keys():
            if self.ethers[net] == layer:
                return net
        Logger.instance.log(Level.ERROR, f"Unable to find network for physical addr {layer.addr}")
        return None

    def pass_up_to_ip(self, packet: Packet, source: EthernetLayer):
        """
        Pass this packet onto the correct IP layer.
        :param source:
        :param packet:
        :return:
        """
        self.ips[source].enqueue(packet)

    def pass_down_to_ether(self, paket: Packet):
        """
        Pass this packet down to the Ethernet layer to be transmitted.
        :param paket:
        :return:
        """