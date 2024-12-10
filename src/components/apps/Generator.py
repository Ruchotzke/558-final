import simpy

from src.components.Node import Node
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Application import Application
from src.utilities.Logger import Logger, Level


class GeneratorApp(Application):
    """
    A simple packet generator.
    """

    def __init__(self, env: simpy.Environment, node: Node, ip: IPAddr, target_port: int, delay=3.0):
        """
        Generate a generator app.
        :param env: The simpy environment
        :param node: The node this will be attached to
        :param ip: The target IP
        :param target_port: The target port
        :param delay: The delay between packets
        """
        # Save the target
        self.target_ip = ip
        self.target_port = target_port
        self.delay = delay

        # Super init
        super().__init__(env, 14311, node.stack)

        # Init name
        self.name = "generator-client"

    def process(self):
        while True:
            yield self.env.timeout(self.delay)
            Logger.instance.log(Level.TRACE, "Hello World")