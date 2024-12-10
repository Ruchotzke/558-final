import simpy

from src.components.stack.IP import IPLayer


class Application:
    """
    Any application running on a node outside of the network stack.
    """

    def __init__(self, env: simpy.Environment, port: int, binding):
        self.env = env
        self.stack = binding
        self.port = port

        # Register this application with the stack
        binding.add_app(port, self)

        # Set up an input and output queue
        self.input = simpy.Store(env)
        self.output = simpy.Store(env)

        # Start the main process (overriden by children)
        env.process(self.process())

    def process(self):
        # By default, do nothing
        return