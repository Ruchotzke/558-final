import simpy

from src.components.Packet import Packet
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Ethernet import EthernetLayer
from typing import List

# Define some types
ifaces = List[EthernetLayer]

class Network:
    """
    A shared resource representing a CSMA network.
    """
    def __init__(self, env: simpy.Environment, net_addr: IPAddr):
        self.env = env          # Environment
        self.nodes: ifaces = []         # Nodes in this network
        self.bandwidth = 100    # Bandwidth of this network (b/s)
        self.active = simpy.Resource(env)   # The mutex for this network
        self.net_addr = net_addr              # This network's IP range

    def __str__(self):
        return f"[net: {self.net_addr}]"

    def register(self, interface: EthernetLayer):
        """
        Register a new node with this local network.
        :param node:
        :return:
        """
        self.nodes.append(interface)

    def proc_send_packet(self, source: EthernetLayer, p: Packet):
        """
        Send a packet into the network: handles delay
        :param source:
        :param p:
        :return:
        """
        # Delay the packet (propagation delay)
        yield self.env.timeout(p.length / self.bandwidth)

        # Handle delivery of packet to all non-sender nodes
        for node in self.nodes:
            if node is not source:
                node.enqueue(p)