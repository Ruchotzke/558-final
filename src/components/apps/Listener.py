import simpy

from src.components.Node import Node
from src.components.Packet import Packet
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Application import Application
from src.utilities.Logger import Logger, Level


class ListenerApp(Application):
    """
    A simple packet generator.
    """

    def __init__(self, env: simpy.Environment, node: Node, listen_port: int):
        """
        Generate a listener app. The app prints a message whenever it receives a transmission
        :param env: The simpy environment
        :param node: The node this will be attached to
        """

        # Super init
        super().__init__(env, listen_port, node.stack)

        # Init name
        self.name = "listener-server"

    def process(self):
        while True:
            # Await an incoming packet
            next: Packet = yield self.input.get()

            # Print a message and discard the packet
            Logger.instance.log(Level.INFO, f"Listener {self.stack.get_default_ip()} received packet from {next.src_ip}")
