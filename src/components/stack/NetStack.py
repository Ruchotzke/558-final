"""
A simple implementation of a network stack.
"""
import simpy

from src.components.Network import Network
from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Application import Application
from src.components.stack.Discipline import PacketDiscipline
from src.components.stack.Ethernet import EthernetLayer
from src.components.stack.IP import IPLayer
from src.components.stack.Tables import RouteTable, ArpTable
from src.utilities.Logger import Logger, Level
from typing import Dict

# Some types
ETHER_LAYERS = Dict[Network, EthernetLayer]
IP_LAYERS = Dict[EthernetLayer, IPLayer]
APPS = Dict[int, Application]


class NetStack:
    """
    A collection of processes representing a host's network stack.
    """

    def __init__(self, env: simpy.Environment):
        self.env = env
        self.ethers: ETHER_LAYERS = {}  # Map of networks to ethernet layers
        self.ips: IP_LAYERS = {}  # Map of ethernet layers to IP layers
        self.apps: APPS = {}  # Map of ports to apps
        self.route_table = RouteTable()  # Route Table
        self.arp_table = ArpTable()  # ARP Cache

    def add_ethernet(self, ether: EthernetAddr, net):
        """
        Add a new Ethernet layer to this stack.
        :param net:
        :param ether:
        :return:
        """
        # Generate a new layer
        layer = EthernetLayer(self.env, ether, self)
        self.ethers[net] = layer
        return layer

    def add_ip(self, ip: IPAddr, ether_layer: EthernetLayer, disc: PacketDiscipline = None):
        """
        Add a new IP layer to this stack.
        :param disc:
        :param ip:
        :param ether_layer:
        :return:
        """
        # Generate a new layer
        layer = IPLayer(self.env, ip, self, disc)
        self.ips[ether_layer] = layer
        return layer

    def add_app(self, port: int, app: Application):
        """
        Add a new application to this stack.
        :param port:
        :param app:
        :return:
        """
        if port in self.apps:
            Logger.instance.log(Level.WARNING, f"Overwriting app on port {port} with new application")
        self.apps[port] = app

    def set_router(self, should_route: bool):
        """
        Configure this device as a router or not
        :param should_route:
        :return:
        """
        for ip in self.ips.values():
            Logger.instance.log(Level.TRACE, f"Reconfiguring {ip.addr} as router.")
            ip.router = should_route

    def get_ip_for_ether(self, ether: EthernetAddr):
        """
        Find the corresponding IP address for an Ethernet address
        :param ether:
        :return:
        """
        for layer in self.ips.keys():
            if layer.addr == ether:
                return self.ips[layer]
        Logger.instance.log(Level.ERROR, f"Unable to map {ether} to an IP address within stack.")
        return None

    def get_ether_for_ip(self, ip: IPAddr):
        """
        Find the corresponding Ethernet interface for an IP address
        :param ip:
        :return:
        """
        for hw in self.ips.keys():
            if self.ips[hw].addr == ip:
                return hw
        Logger.instance.log(Level.ERROR, f"Unable to map {ip} to an Ethernet address within stack.")
        return None

    def get_ip(self, ip: IPAddr):
        """
        Get the IP layer for a given address.
        :param ip:
        :return:
        """
        for iface in self.ips.values():
            if iface.addr == ip:
                return iface
        Logger.instance.log(Level.ERROR, f"Unable to map {ip} to an IP address within stack.")
        return None

    def get_network(self, layer: EthernetLayer):
        for net in self.ethers.keys():
            if self.ethers[net] == layer:
                return net
        Logger.instance.log(Level.ERROR, f"Unable to find network for physical addr {layer.addr}")
        return None

    def pass_up_to_ip(self, packet: Packet, source: EthernetLayer):
        """
        Pass this packet onto the correct IP layer.
        :param source:
        :param packet:
        :return:
        """
        Logger.instance.log(Level.TRACE, f"{source.addr} passing packet to {self.ips[source].addr}")
        self.ips[source].enqueue(packet)

    def pass_up_to_app(self, packet: Packet):
        """
        Pass this packet up to an application.
        :param packet:
        :return:
        """
        if packet.dst_port not in self.apps:
            Logger.instance.log(Level.WARNING, f"Unable to match app for port {packet.dst_port}. Discarding.")
            return
        self.apps[packet.dst_port].input.put(packet)

    def pass_down_to_ether(self, packet: Packet, iface: EthernetLayer):
        """
        Pass this packet down to the Ethernet layer to be transmitted.
        :param iface:
        :param packet:
        :return:
        """
        # Find the right interface
        Logger.instance.log(Level.TRACE, f"{packet} sent to {iface.addr} for transmission")
        iface.stack_in_queue.put(packet)

    def send(self, p: Packet):
        """
        High level send function for sending a packet over the network via an app.
        :param p:
        :return:
        """
        # find the correct interface to send from
        hw = self.get_ip(p.src_ip)

        # pass the packet on
        hw.to_send_queue.put(p)

    def get_default_ip(self):
        """
        Get the default IP (first one in interfaces).
        Useful for apps
        :return:
        """
        return list(self.ips.values())[0].addr
