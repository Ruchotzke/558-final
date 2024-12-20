import simpy

from src.components.Node import Node
from src.components.Packet import Packet
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Application import Application
from src.utilities.Logger import Logger, Level


class LogServerApp(Application):
    """
    A listener which logs packet timings to a file.
    """

    def __init__(self, env: simpy.Environment, node: Node, listen_port: int, file):
        """
        Generate a listener app. The app prints a message whenever it receives a transmission
        :param env: The simpy environment
        :param node: The node this will be attached to
        """

        self.file = file

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

            # Log the packet to a file
            with open(self.file, "a") as fd:
                fd.write(f"{self.env.now},{next.length},{next.msg},{next.id}\n")