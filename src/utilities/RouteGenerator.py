"""
A set of utilities for filling in route/ARP tables
"""
from typing import List
from src.components.Network import Network
from src.components.Node import Node
from src.components.stack.Tables import ArpEntry, RouteEntry
from src.utilities.Logger import Logger, Level

# Define a type
NETS = List[Network]
ARPENTR = List[ArpEntry]

def update_routes(networks: NETS):
    """
    Update the routes for everything on every network.
    :param networks:
    :return:
    """
    # Easy: Start with ARP entries
    for net in networks:
        entries: ARPENTR = []

        # Get all entries
        for dev in net.nodes:
            # Get the corresponding IP
            ip = dev.stack.get_ip_for_ether(dev.addr).addr
            entries.append(ArpEntry(ip, dev.addr))

        # Populate all entries
        for dev in net.nodes:
            for entry in entries:
                dev.stack.arp_table.add_entry(entry)

        # Debug
        Logger.instance.log(Level.DEBUG, f"Finished ARP setup for {net}")

    # Basic Routing: Generate everyone's default entries to be the router (SINGLE) on their network
    # TODO: Expand this to multiple routers/real networks
    for net in networks:
        # Find the router
        router = None
        for dev in net.nodes:
            if list(dev.stack.ips.values())[0].router:
                router = list(dev.stack.ips.values())[0].addr
                break
        if router is None:
            Logger.instance.log(Level.ERROR, f"Unable to find router on {net}")

        # Set default gateways
        for dev in net.nodes:
            dev.stack.route_table.default = RouteEntry(None, router, dev)

        # Debugs
        Logger.instance.log(Level.DEBUG, f"Finished Route setup for {net}")
