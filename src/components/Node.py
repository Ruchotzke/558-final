"""
An implementation of a network node.
"""
import simpy

from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.stack.NetStack import NetStack
from src.utilities.Logger import Logger


class Node:
    """
    A node in a network.
    """
    def __init__(self, env: simpy.Environment, name):
        self.env = env
        self.name = name
        self.stack = NetStack(env)
        Logger.instance.log(f'Node {self.name} initialized.')

    def start_process(self):
        self.env.process(self.produce())

    def add_interface(self, network):
        """
        Add an interface to this node.
        :param network:
        :return:
        """
        self.stack.add_ethernet(EthernetAddr("11:11:11:11:11:11"), network)
        network.register(self)


    def recv(self, p: Packet, source_net):
        """
        Receive a packet from the network
        :param p:
        :return:
        """
        # Packet arrived
        Logger.instance.log(f'Node {self.name} received a packet: pushing to stack')

        # Sort and send to proper interface
        self.stack.ethers[source_net].queue.put(p)


    def produce(self):
        while True:
            yield self.env.timeout(10.0)
            self.env.process(self.push_packet(list(self.stack.ethers.keys())[0]))

    def push_packet(self, network):
        with network.active.request() as req:
            # Await access to the network
            yield req

            # Push a packet out over the networks
            Logger.instance.log(f'Node {self.name} pushed out a packet')
            yield self.env.process(network.send_packet(self, Packet(45.0, "hello", EthernetAddr())))
