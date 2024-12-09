"""
A simple packet abstraction.
"""
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr


class Packet:
    def __init__(self, length: float, msg, ether: EthernetAddr, ip = IPAddr):
        """
        Initialize a new packet.
        :param msg: The contained message.
        """
        self.length = length
        self.msg = msg
        self.ether = ether
        self.ip = ip
