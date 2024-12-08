"""
A simple packet abstraction.
"""
from src.components.addressing.EthernetAddr import EthernetAddr


class Packet:
    def __init__(self, length: float, msg, ether: EthernetAddr):
        """
        Initialize a new packet.
        :param msg: The contained message.
        """
        self.length = length
        self.msg = msg
        self.ether = ether
