"""
An implementation of a network node.
"""
import simpy

from Packet import Packet


class Node:
    """
    A node in a network.
    """
    def __init__(self, env: simpy.Environment, name):
        self.env = env
        self.interfaces = []
        self.name = name

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
        print(f'Node {self.name} received a packet at t={self.env.now}')

    def produce(self):
        while True:
            yield self.env.timeout(2.0)
            self.env.process(self.push_packet(self.interfaces[0]))

    def push_packet(self, network):
        with network.active.request() as req:
            # Await access to the network
            yield req

            # Push a packet out over the network
            print(f'Node {self.name} pushed out a packet at {self.env.now}')
            yield self.env.process(network.send_packet(self, Packet(45.0, "hello")))
