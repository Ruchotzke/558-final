from typing import List

from src.components.Packet import Packet
from src.components.addressing.IPAddr import IPAddr
from src.components.stack.Discipline import PacketDiscipline, Flow
from src.utilities import Delays
from src.utilities.Logger import Logger, Level


class RoundRobinDiscipline(PacketDiscipline):
    """
    A basic round-robin scheduler
    """

    def __init__(self, file):
        super().__init__(file)
        self.left_off = 0

    def init_flows(self, flows: List[IPAddr], use_default: bool):
        self.use_default = use_default
        for ip in flows:
            new_flow = Flow(ip)
            self.flows.append(new_flow)

    def proc_handle_disc(self):
        while True:
            # delay until the output queue is empty (on-demand)
            if len(self.output_queue.items) == 0:
                # Perform basic RR on all queues until we get an item
                for i in range(0, len(self.flows) + 1):
                    # Get the queue index
                    idx = (i + self.left_off + 1) % (len(self.flows) + 1)

                    # Handle this queue
                    if idx == len(self.flows):
                        if self.use_default:
                            # Default queue
                            if len(self.default.queue) > 0:
                                next = self.default.queue[0]
                                self.default.queue.pop(0)
                                self.output_queue.put(next)
                                self.left_off = idx
                                if self.file is not None:
                                    with open(self.file, "a") as fd:
                                        fd.write(f"{self.env.now}, DEQUEUE {self.default.match}, {next.length}\n")
                                break
                    else:
                        # Normal queue
                        if len(self.flows[idx].queue) > 0:
                            next = self.flows[idx].queue[0]
                            self.flows[idx].queue.pop(0)
                            self.output_queue.put(next)
                            self.left_off = idx
                            if self.file is not None:
                                with open(self.file, "a") as fd:
                                    fd.write(f"{self.env.now}, DEQUEUE {self.flows[idx].match}, {next.length}\n")
                            break
            yield self.env.timeout(Delays.ROUND_ROBIN_DELAY())



