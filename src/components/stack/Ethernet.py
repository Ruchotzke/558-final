import simpy

from src.components.Packet import Packet
from src.components.addressing.EthernetAddr import EthernetAddr
from src.utilities.Logger import Logger, Level


class EthernetLayer:
    """
    An Ethernet layer implementation.
    """

    def __init__(self, env: simpy.Environment, addr: EthernetAddr, stack):
        self.env = env              # Simpy environment
        self.addr = addr            # Associated Ethernet layer addr
        self.promiscuous = False    # Promiscuous mode (sniffing)
        self.queue = simpy.Store(env)   # The input queue
        self.stack = stack          # Network stack
        env.process(self.process())

    def enqueue(self, p: Packet):
        self.queue.put(p)

    def process(self):
        while True:
            # Await the next packet
            next: Packet = yield self.queue.get()

            # Check if the address matches
            if self.promiscuous or self.addr.filter(next.ether):
                # Packet can be processed.
                Logger.instance.log(Level.TRACE, f'{self.addr} received packet.')

                # Push up to IP
                self.stack.pass_up_to_ip(next, self)
            else:
                # packet is deleted
                Logger.instance.log(Level.DEBUG, f'Ethernet layer {self.addr} ignoring packet with addr {next.ether}')
