from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Ethernet import EthernetLayer
from src.utilities.Logger import Logger, Level
from typing import List

# Define some types for use in annotation
ArpTableContents = list["ArpEntry"]
RouteTableContents = list["RouteEntry"]


class RouteEntry:
    """
    Entry in the route table
    """

    def __init__(self, network: IPAddr, next: IPAddr, iface: EthernetLayer):
        self.network: IPAddr = network
        self.next_hop: IPAddr = next
        self.iface: EthernetLayer = iface

    def __str__(self):
        return f"[{self.network}: {self.next_hop}, {self.iface.addr}]"


class ArpEntry:
    """
    Entry in the ARP table
    """

    def __init__(self, ip: IPAddr, hw: EthernetAddr):
        self.ip = ip
        self.ether = hw

    def __str__(self):
        return f"[{self.ip} -> {self.ether}]"


class RouteTable:
    """
    A simple route table implementation
    """

    tables = []
    """
    A set of all tables in the simulation.
    """

    def __init__(self):
        self.table: RouteTableContents = []
        RouteTable.tables.append(self)
        self.default: RouteEntry = None

    def __del__(self):
        RouteTable.tables.remove(self)

    def insert_entry(self, route_entry: RouteEntry):
        self.table.append(route_entry)

    def search(self, network: IPAddr):
        entries = [a for a in self.table if a.network == network]
        if len(entries) == 0:
            if self.default is None:
                Logger.instance.log(Level.DEBUG, f"Cannot find route entry for network {network}, missing default")
                return None
            else:
                Logger.instance.log(Level.TRACE, f"Default route returned for {network} query")
                return self.default
        if len(entries) > 1:
            Logger.instance.log(Level.DEBUG, f"Found multiple route entries for network {network}")
        return entries[0]


class ArpTable:
    """
    A simple ARP table implementation
    """

    def __init__(self):
        self.table: ArpTableContents = []

    def add_entry(self, entry: ArpEntry):
        Logger.instance.log(Level.DEBUG, f"Added arp entry {entry}")
        self.table.append(entry)

    def search(self, ip: IPAddr):
        entries = [a for a in self.table if a.ip == ip]
        if len(entries) == 0:
            Logger.instance.log(Level.DEBUG, f"Cannot find ARP entry for IP {ip}")
            return None
        if len(entries) > 1:
            Logger.instance.log(Level.DEBUG, f"Found multiple ARP entries for IP {ip}")
        return entries[0]
