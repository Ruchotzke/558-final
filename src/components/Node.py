"""
An implementation of a network node.
"""
import simpy

from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.utilities.Logger import Logger


class Node:
    """
    A node in a network.
    """
    def __init__(self, env: simpy.Environment, name):
        self.env = env
        self.interfaces = []
        self.name = name
        Logger.instance.log(f'Node {self.name} initialized.')

    def start_process(self):
        self.env.process(self.produce())

    def add_interface(self, network, local_addr, global_addr):
        """
        Add an interface to this node.
        :param network:
        :return:
        """
        self.interfaces.append(network)
        network.register(self)


    def recv(self, p: Packet):
        """
        Receive a packet from the network
        :param p:
        :return:
        """
        Logger.instance.log(f'Node {self.name} received a packet')

    def produce(self):
        while True:
            yield self.env.timeout(2.0)
            self.env.process(self.push_packet(self.interfaces[0]))

    def push_packet(self, network):
        with network.active.request() as req:
            # Await access to the network
            yield req

            # Push a packet out over the networks
            Logger.instance.log(f'Node {self.name} pushed out a packet')
            yield self.env.process(network.send_packet(self, Packet(45.0, "hello", EthernetAddr())))
