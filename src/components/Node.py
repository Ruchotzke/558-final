"""
An implementation of a network node.
"""
import simpy

from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.NetStack import NetStack
from src.utilities.Logger import Logger, Level


class Node:
    """
    A node in a network.
    """
    def __init__(self, env: simpy.Environment, name):
        self.env = env
        self.name = name
        self.stack = NetStack(env)
        Logger.instance.log(Level.TRACE, f'Node {self.name} initialized.')

    def start_process(self, target: (EthernetAddr, IPAddr)):
        self.env.process(self.produce(target))

    def add_interface(self, network, ether: EthernetAddr, ip: IPAddr):
        """
        Add an interface to this node.
        :param ether:
        :param ip:
        :param network:
        :return:
        """
        hw_layer = self.stack.add_ethernet(ether, network)
        network.register(self)
        self.stack.add_ip(ip, hw_layer)

    def recv(self, p: Packet, source_net):
        """
        Receive a packet from the network
        :param p:
        :return:
        """
        # Packet arrived
        Logger.instance.log(Level.DEBUG, f'Node {self.name} received a packet: pushing to stack')

        # Sort and send to proper interface
        self.stack.ethers[source_net].queue.put(p)

    def produce(self, target_addrs: (EthernetAddr, IPAddr)):
        while True:
            # Figure out a network and address
            net = list(self.stack.ethers.keys())[0]
            packet = Packet(100, "hello", target_addrs[0], target_addrs[1])

            # Send the packet
            self.env.process(self.push_packet(net, packet))

            # Wait for the next round of outputs
            yield self.env.timeout(5.0)

    def push_packet(self, network, packet):
        with network.active.request() as req:
            # Await access to the network
            yield req

            # Push a packet out over the networks
            Logger.instance.log(Level.DEBUG, f'Node {self.name} pushed out a packet')
            yield self.env.process(network.send_packet(self, packet))
