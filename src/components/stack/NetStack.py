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

    def __init__(self, env: simpy.Environment, ether: EthernetAddr):
        self.ether = EthernetLayer(env, ether)
        