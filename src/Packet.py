"""
A simple packet abstraction.
"""


class Packet:
    def __init__(self, length: float, msg):
        """
        Initialize a new packet.
        :param msg: The contained message.
        """
        self.length = length
        self.msg = msg

