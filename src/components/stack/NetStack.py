"""
A simple implementation of a network stack.
"""
import simpy

from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Ethernet import EthernetLayer
from src.components.stack.IP import IPLayerStandard


class NetStack:
    """
    A collection of processes representing a host's network stack.
    """

    def __init__(self, env: simpy.Environment):
        self.env = env
        self.ethers = {}    # Map of networks to ethernet layers
        self.ips = {}       # Map of ethernet layers to IP layers
        self.apps = []

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
        layer = IPLayerStandard(self.env, ip, self)
        self.ips[ether_layer] = layer
        return layer

    def pass_up_to_ip(self, packet: Packet, source: EthernetLayer):
        """
        Pass this packet onto the correct IP layer.
        :param source:
        :param packet:
        :return:
        """
        self.ips[source].enqueue(packet)
