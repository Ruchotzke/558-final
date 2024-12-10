import simpy

from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.utilities import Delays
from src.utilities.Logger import Logger, Level


class EthernetLayer:
    """
    An Ethernet layer implementation.
    """

    def __init__(self, env: simpy.Environment, addr: EthernetAddr, stack):
        self.env = env              # Simpy environment
        self.addr = addr            # Associated Ethernet layer addr
        self.promiscuous = False    # Promiscuous mode (sniffing)
        self.net_in_queue = simpy.Store(env)    # The input queue from the network
        self.stack_in_queue = simpy.Store(env)  # The input queue from the upper part of the stack
        self.stack = stack          # Network stack
        env.process(self.recv_process())    # Network Receiver
        env.process(self.send_process())    # Stack Receiver

    def enqueue(self, p: Packet):
        Logger.instance.log(Level.INFO, f"Interface {self.addr} recieved packet from network.")
        self.net_in_queue.put(p)

    def recv_process(self):
        while True:
            # Await the next packet
            next: Packet = yield self.net_in_queue.get()

            # Queue delay
            yield self.env.timeout(Delays.HW_QUEUE_DELAY())

            # Check if the address matches
            if self.promiscuous or self.addr.filter(next.dst_ether):
                # Packet can be processed.
                Logger.instance.log(Level.INFO, f'{self.addr} accepted packet.')

                # Push up to IP
                self.stack.pass_up_to_ip(next, self)
            else:
                # packet is deleted
                Logger.instance.log(Level.DEBUG, f'Ethernet layer {self.addr} ignoring packet with addr {next.dst_ether}')

    def send_process(self):
        while True:
            # Await the next packet
            next: Packet = yield self.stack_in_queue.get()

            # Queue delay
            yield self.env.timeout(Delays.HW_QUEUE_DELAY())

            # Update source Ethernet address
            next.src_ether = self.addr

            # Get a reference to the connected network
            net = self.stack.get_network(self)

            # Await the shared resource
            with net.active.request() as req:
                yield req

                # Push the packet out
                Logger.instance.log(Level.DEBUG, f'Interface {self.addr} pushed out a packet')
                yield self.env.process(net.proc_send_packet(self, next))
