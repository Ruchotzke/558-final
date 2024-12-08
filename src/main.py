import simpy

from src.components.Node import Node
from src.components.Network import Network
from src.utilities.Logger import Logger

env = simpy.Environment()

# Init the logger
logger = Logger()
logger.init_instance(env)

N1 = Node(env, "N1")
N2 = Node(env, "N2")
net = Network(env)

N1.add_interface(net)
N2.add_interface(net)

N1.start_process()
N2.start_process()

env.run(until=15)