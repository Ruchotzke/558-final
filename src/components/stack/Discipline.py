from typing import List, Tuple, Dict

import simpy

from src.components.Packet import Packet
from src.components.addressing.IPAddr import IPAddr
from src.utilities.Logger import Logger, Level


class Flow:
    """
    A packet flow.
    """

    def __init__(self, match: IPAddr):
        self.match = match
        self.queue: List[Packet] = []
        self.properties: Dict[str, float] = {}


class PacketDiscipline:
    """
    A manager for what order/how fast to process packets.
    Consists of at least one flow, a processor, and an output.
    """

    def __init__(self):
        self.default = Flow(IPAddr("0.0.0.0"))
        self.use_default = True
        self.env: simpy.Environment = None
        self.output_queue: simpy.Store = None
        self.flows: List[Flow] = []

    def init_flows_weighted(self, flows: List[Tuple[IPAddr, float]], default_weight: float):
        """
        Initialize this discipline with a set of flows and weights.
        :param default_weight: The weight for the default queue (0 disables it)
        :param flows:
        :return:
        """
        return

    def init_flows(self, flows: List[IPAddr], use_default: bool):
        """
        Initialize this discipline with a set of flows
        :param flows: The flows to initialize
        :param use_default: Whether or not non-flows queue is enabled.
        :return:
        """
        return

    def enqueue_packet(self, p: Packet):
        """
        Enqueue a packet to this discipline.
        :param p:
        :return:
        """
        # Check across matching flows
        for flow in self.flows:
            if flow.match == p.src_ip:
                # Use this flow
                flow.queue.append(p)
                return

        # If we didn't find a queue, try default
        if self.use_default:
            self.default.queue.append(p)
        else:
            Logger.instance.log(Level.DEBUG, f"Discipline is not configured to use default and is destroying {p}")

    def proc_handle_disc(self):
        return

    def init_proc(self, env: simpy.Environment, queue: simpy.Store):
        """
        Initialize this disc. process.
        :param env:
        :param queue:
        :return:
        """
        self.output_queue = queue
        self.env = env
        env.process(self.proc_handle_disc())