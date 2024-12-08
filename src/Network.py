import simpy

from Node import Node
from Packet import Packet


class Network:
    """
    A shared resource representing a CSMA network.
    """
    def __init__(self, env: simpy.Environment):
        self.env = env          # Environment
        self.nodes = []         # Nodes in this network
        self.bandwidth = 100    # Bandwidth of this network (b/s)
        self.active = simpy.Resource(env)   # The mutex for this network

    def register(self, node):
        """
        Register a new node with this local network.
        :param node:
        :return:
        """
        self.nodes.append(node)

    def send_packet(self, source: Node, p: Packet):
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
            if node != source:
                node.recv(p)