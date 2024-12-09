import simpy

from src.components.Node import Node
from src.components.Network import Network
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.utilities import RouteGenerator
from src.utilities.Logger import Logger

env = simpy.Environment()

# Init the logger
logger = Logger()
logger.init_instance(env)

#
# Network Vision
#
#  1         2         3
# N1        N2        N3
#  |        ||        |
#   ========  ========
#    x.x.0.0   x.x.1.0


# Generate left network
N1 = Node(env, "N1")
N2 = Node(env, "N2")
left_net = Network(env, IPAddr("192.168.0.0"))

N1.add_interface(left_net, EthernetAddr("00:11:11:11:11:11"), IPAddr("192.168.0.1"))
N2.add_interface(left_net, EthernetAddr("00:22:22:22:22:22"), IPAddr("192.168.0.2"))

# Generate right network
N3 = Node(env, "N3")
right_net = Network(env, IPAddr("192.168.1.0"))

N2.add_interface(right_net, EthernetAddr("11:22:22:22:22:22"), IPAddr("192.168.1.2"))
N3.add_interface(right_net, EthernetAddr("11:33:33:33:33:33"), IPAddr("192.168.1.3"))

# Network setup
nets = [left_net, right_net]
RouteGenerator.update_routes(nets)

# Start Processes
# N1.start_process((EthernetAddr("11:33:33:33:33:33"), IPAddr("192.168.1.3")))
# N2.start_process((EthernetAddr("FF:FF:FF:FF:FF:FF"), IPAddr("192.168.0.3")))
N3.start_process((EthernetAddr("11:22:22:22:22:22"), IPAddr("192.168.0.2")))

env.run(until=8)