"""
A simple packet abstraction.
"""
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr


class Packet:
    def __init__(self, length: float, msg: str, src_ether: EthernetAddr, dst_ether: EthernetAddr,
                 src_ip: IPAddr, dst_ip: IPAddr,
                 src_port: int, dst_port: int):
        """
        Initialize a new packet.
        :param msg: The contained message.
        """
        self.length = length
        self.src_ether = src_ether
        self.dst_ether = dst_ether
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port

        self.msg = msg

    def __str__(self):
        return f"[pkt: {self.msg}: src ->[{self.src_ether},{self.src_ip}], dst->[{self.dst_ether},{self.dst_ip}]]"
