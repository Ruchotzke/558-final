"""
A set of utilities for filling in route/ARP tables
"""
from typing import List
from src.components.Network import Network
from src.components.stack.Tables import ArpEntry
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