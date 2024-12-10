import sys
from typing import List, Dict

from src.components.Packet import Packet
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Discipline import PacketDiscipline, Flow
from src.utilities import Delays
from src.utilities.Logger import Logger, Level


class FQDiscipline(PacketDiscipline):
    """
    A basic fair-queue (FQ) scheduler
    """

    def __init__(self):
        super().__init__()
        self.left_off = 0
        self.virt_finishes: Dict[Packet, float] = {}

    def init_flows(self, flows: List[IPAddr], use_default: bool):
        self.use_default = use_default
        for ip in flows:
            new_flow = Flow(ip)
            new_flow.properties["vir_fin"] = 0
            self.flows.append(new_flow)

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

                # Handle finish times
                vir_start = max(self.env.now, flow.properties["vir_fin"])
                self.virt_finishes[p] = p.length + vir_start
                flow.properties["vir_fin"] = self.virt_finishes[p]
                return

        # If we didn't find a queue, try default
        if self.use_default:
            self.default.queue.append(p)
        else:
            Logger.instance.log(Level.DEBUG, f"Discipline is not configured to use default and is destroying {p}")

    def proc_handle_disc(self):
        while True:
            # delay until the output queue is empty (on-demand)
            if len(self.output_queue.items) == 0:
                # Send the packet with the lowest finish time (of any queue)
                # Find the minimal
                min = sys.float_info.max
                idx = None
                for i in range(0, len(self.flows)):
                    if len(self.flows[i].queue) > 0:
                        if self.virt_finishes[self.flows[i].queue[0]] < min:
                            min = self.virt_finishes[self.flows[i].queue[0]]
                            idx = i

                # If it exists (it may not), send it
                if idx is not None:
                    pkt = self.flows[idx].queue[0]
                    self.flows[idx].queue.pop()
                    self.output_queue.put(pkt)
            yield self.env.timeout(Delays.ROUND_ROBIN_DELAY())

