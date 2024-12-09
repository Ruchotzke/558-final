"""
An implementation of a network node.
"""
import simpy

from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.NetStack import NetStack
from src.components.stack.Tables import RouteEntry
from src.utilities.Logger import Logger, Level
from typing import List

# Define some types
NODE_SET = List["Node"]


class Node:
    """
    A node in a network.
    """

    nodes: NODE_SET = []
    """
    A set of all nodes in the simulation.
    """


    def __init__(self, env: simpy.Environment, name):
        self.env = env
        self.name = name
        self.stack = NetStack(env)
        Node.nodes.append(self)
        Logger.instance.log(Level.TRACE, f'Node {self.name} initialized.')

    def __del__(self):
        Node.nodes.remove(self)

    def start_process(self, target: (EthernetAddr, IPAddr)):
        self.env.process(self.produce(target))

    def add_interface(self, network, ether: EthernetAddr, ip: IPAddr, netm: IPAddr = IPAddr("255.255.255.0")):
        """
        Add an interface to this node.
        :param netm:
        :param ether:
        :param ip:
        :param network:
        :return:
        """
        # Add the layers
        hw_layer = self.stack.add_ethernet(ether, network)
        network.register(hw_layer)
        self.stack.add_ip(ip, hw_layer)

        # Apply the netmask
        net_addr = ip.apply_netmask(netm)
        Logger.instance.log(Level.TRACE, f"Added interface {ether}, {ip} to {self.name}")

        # Update the route table to reflect new direct entries
        entry = RouteEntry(net_addr, ip, hw_layer)
        entry.direct = True
        self.stack.route_table.insert_entry(entry)
        Logger.instance.log(Level.TRACE, f"Generated new route entry: {entry} to {self.name}")

    def recv(self, p: Packet, source_net):
        """
        Receive a packet from the network
        :param source_net:
        :param p:
        :return:
        """
        # Packet arrived
        Logger.instance.log(Level.DEBUG, f'Node {self.name} received a packet: pushing to stack')

        # Sort and send to proper interface
        self.stack.ethers[source_net].net_in_queue.put(p)

    def produce(self, target_addrs: (EthernetAddr, IPAddr)):
        while True:
            # Figure out a network and address
            net = list(self.stack.ethers.keys())[0]
            src_ip = list(self.stack.ips.values())[0].addr
            src_hw = list(self.stack.ethers.values())[0].addr
            packet = Packet(100, "hello", src_hw, target_addrs[0], src_ip, target_addrs[1])

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
            yield self.env.process(network.proc_send_packet(self, packet))
