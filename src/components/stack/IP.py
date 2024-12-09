import simpy

from src.components.Packet import Packet
from src.components.addressing.IPAddr import IPAddr
from src.utilities.Logger import Logger, Level


class IPLayerStandard:
    """
    A standard IP layer. Non-matching packets are discarded.
    """
    def __init__(self, env: simpy.Environment, addr: IPAddr, stack):
        self.env = env              # Simpy environment
        self.addr = addr            # Associated IP layer addr
        self.queue = simpy.Store(env)   # The input queue
        self.stack = stack              # Network stack
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
                Logger.instance.log(Level.DEBUG, f"IP Layer {self.addr} ignoring packet for {next.ip}.")

class IPLayerRouter:
    """
    An IP layer which forwards, rather than discards, non-matching packets.
    """