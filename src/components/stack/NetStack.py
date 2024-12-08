"""
A simple implementation of a network stack.
"""
import simpy

from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.stack.Ethernet import EthernetLayer


class NetStack:
    """
    A collection of processes representing a host's network stack.
    """

    def __init__(self, env: simpy.Environment):
        self.env = env
        self.ethers = {}
        self.ips = []
        self.apps = []

    def add_ethernet(self, ether: EthernetAddr, net):
        """
        Add a new Ethernet layer to this stack.
        :param net:
        :param ether:
        :return:
        """
        # Generate a new layer
        layer = EthernetLayer(self.env, ether)
        self.ethers[net] = layer
