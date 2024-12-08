import simpy

from src.components.Node import Node
from src.components.Network import Network
from src.components.addressing.EthernetAddr import EthernetAddr
from src.utilities.Logger import Logger

env = simpy.Environment()

# Init the logger
logger = Logger()
logger.init_instance(env)

N1 = Node(env, "N1")
N2 = Node(env, "N2")
N3 = Node(env, "N3")
net = Network(env)

N1.add_interface(net, EthernetAddr("11:11:11:11:11:11"))
N2.add_interface(net, EthernetAddr("22:22:22:22:22:22"))
N3.add_interface(net, EthernetAddr("33:33:33:33:33:33"))

N1.start_process(EthernetAddr("22:22:22:22:22:22"))
N2.start_process(EthernetAddr("FF:FF:FF:FF:FF:FF"))
N3.start_process(EthernetAddr("22:22:22:22:22:22"))

env.run(until=8)