import simpy

from src.components.Packet import Packet
from src.components.addressing.IPAddr import IPAddr
from src.components.disciplines.RoundRobin import RoundRobinDiscipline
from src.components.stack.Discipline import PacketDiscipline
from src.components.stack.Tables import RouteTable, ArpTable
from src.utilities import Delays
from src.utilities.Logger import Logger, Level


class IPLayer:
    """
    A standard IP layer. Non-matching packets are routed if configured to do so.
    """
    def __init__(self, env: simpy.Environment, addr: IPAddr, stack, disc: PacketDiscipline = None):
        self.env = env              # Simpy environment
        self.addr = addr            # Associated IP layer addr
        self.to_process_queue = simpy.Store(env)   # The input queue
        self.to_send_queue = simpy.Store(env)       # The output queue
        self.stack = stack              # Network stack
        self.router = False             # Should this layer route packets

        if disc is not None:
            self.discipline = disc
            self.discipline.init_proc(env, self.to_send_queue)
            self.ignore_disc = False
        else:
            self.ignore_disc = True

        env.process(self.proc_handle_inputs())
        env.process(self.proc_handle_outputs())

        Logger.instance.log(Level.DEBUG, f"{addr} is{' ' if not self.ignore_disc else 'not '}using a discipline")

    def enqueue(self, p: Packet):
        self.to_process_queue.put(p)

    def proc_handle_inputs(self):
        while True:
            # Grab the next packet from the queue
            next: Packet = yield self.to_process_queue.get()

            # Queue delay
            yield self.env.timeout(Delays.IP_QUEUE_DELAY())

            # Check/filter the IP address
            if next.dst_ip == self.addr:
                # Forward the packet to the applications
                Logger.instance.log(Level.TRACE, f"IP Layer {self.addr} processing packet.")

                # Queue delay
                yield self.env.timeout(Delays.APP_QUEUE_DELAY())

                self.stack.pass_up_to_app(next)
            else:
                if not self.router:
                    # Throw away the packet
                    Logger.instance.log(Level.DEBUG, f"IP Layer {self.addr} ignoring packet for {next.dst_ip}.")
                else:
                    # The packet needs to be routed: put it into output queue
                    Logger.instance.log(Level.DEBUG, f"IP Layer {self.addr} moving packet for {next.dst_ip} to output queue.")
                    if self.ignore_disc:
                        self.to_send_queue.put(next)
                    else:
                        self.discipline.enqueue_packet(next)


    def proc_handle_outputs(self):
        while True:
            # Grab the next packet from the queue
            next: Packet = yield self.to_send_queue.get()

            # Queue delay
            yield self.env.timeout(Delays.IP_QUEUE_DELAY())

            # Attempt to route the packet
            Logger.instance.log(Level.DEBUG, f"IP Layer {self.addr} attempting to route packet for {next.dst_ip}.")

            # Check route table
            route = self.stack.route_table.search(next.dst_ip.apply_netmask(IPAddr("255.255.255.0")))
            if route is None:
                Logger.instance.log(Level.DEBUG, f"IP Layer {self.addr} failed to route packet for {next.dst_ip}.")

            # Figure out a target IP based on whether or not the entry is direct
            target = next.dst_ip if route.direct else route.next_hop

            # Check ARP table
            arp_entry = self.stack.arp_table.search(target)
            if arp_entry is None:
                Logger.instance.log(Level.DEBUG, f"IP Layer {self.addr} failed to ARP lookup address {route.next_hop}")

            # Transmit the packet
            next.dst_ether = arp_entry.ether
            yield self.env.process(self.stack.proc_pass_down_to_ether(next, route.iface))