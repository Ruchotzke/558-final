import simpy

from src.components.Packet import Packet
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Tables import RouteTable, ArpTable
from src.utilities.Logger import Logger, Level


class IPLayer:
    """
    A standard IP layer. Non-matching packets are routed if configured to do so.
    """
    def __init__(self, env: simpy.Environment, addr: IPAddr, stack):
        self.env = env              # Simpy environment
        self.addr = addr            # Associated IP layer addr
        self.queue = simpy.Store(env)   # The input queue
        self.stack = stack              # Network stack
        self.router = False             # Should this layer route packets
        env.process(self.process())

    def enqueue(self, p: Packet):
        self.queue.put(p)

    def process(self):
        while True:
            # Grab the next packet from the queue
            next: Packet = yield self.queue.get()

            # Check/filter the IP address
            if next.ip == self.addr:
                # Forward the packet to the applications
                Logger.instance.log(Level.TRACE, f"IP Layer {self.addr} processing packet.")
            else:
                if not self.router:
                    # Throw away the packet
                    Logger.instance.log(Level.DEBUG, f"IP Layer {self.addr} ignoring packet for {next.ip}.")
                else:
                    # Attempt to route the packet
                    Logger.instance.log(Level.DEBUG, f"IP Layer {self.addr} attempting to route packet for {next.ip}.")

                    # Check route table
                    route = self.stack.route_table.search(next.ip.apply_netmask(IPAddr("255.255.255.0")))
                    if route is None:
                        Logger.instance.log(Level.DEBUG,f"IP Layer {self.addr} failed to route packet for {next.ip}.")

                    # Figure out a target IP based on whether or not the entry is direct
                    target = next.ip if route.direct else route.next_hop

                    # Check ARP table
                    arp_entry = self.stack.arp_table.search(target)
                    if arp_entry is None:
                        Logger.instance.log(Level.DEBUG, f"IP Layer {self.addr} failed to ARP lookup address {route.next_hop}")

                    # Transmit the packet
                    next.ether = arp_entry.ether
                    self.stack.pass_down_to_ether(next, route.iface)