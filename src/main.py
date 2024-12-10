import simpy

from src.components.Node import Node
from src.components.Network import Network
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.components.apps.Generator import GeneratorApp
from src.components.apps.Listener import ListenerApp
from src.utilities import RouteGenerator
from src.utilities.Logger import Logger, Level

env = simpy.Environment()

# Init the logger
logger = Logger()
logger.init_instance(env)
logger.instance.LOG_LEVEL = Level.DEBUG

#
# Network Vision
#
# N1 N2 N3  R1        S1
#  |  |  |  ||        |
#   ========  ========
#    x.x.0.0   x.x.1.0


# Generate left network
N1 = Node(env, "N1")
N2 = Node(env, "N2")
N3 = Node(env, "N3")
left_net = Network(env, IPAddr("192.168.0.0"))

N1.add_interface(left_net, EthernetAddr("00:11:11:11:11:11"), IPAddr("192.168.0.1"))
N2.add_interface(left_net, EthernetAddr("00:22:22:22:22:22"), IPAddr("192.168.0.2"))
N3.add_interface(left_net, EthernetAddr("00:33:33:33:33:33"), IPAddr("192.168.0.3"))

# Generate right network
S1 = Node(env, "S1")
right_net = Network(env, IPAddr("192.168.1.0"))

S1.add_interface(right_net, EthernetAddr("11:FF:FF:FF:FF:FF"), IPAddr("192.168.1.1"))

# Generate router
R1 = Node(env, "R1")
R1.add_interface(left_net, EthernetAddr("00:44:44:44:44:44"), IPAddr("192.168.0.254"))
R1.add_interface(right_net, EthernetAddr("11:44:44:44:44:44"), IPAddr("192.168.1.254"))
R1.stack.set_router(True)

# Network setup
nets = [left_net, right_net]
RouteGenerator.update_routes(nets)

# Install an app
app = GeneratorApp(env, N1, IPAddr("192.168.1.1"), 22)
N1.install_app(app)
app2 = ListenerApp(env, S1, 22)
S1.install_app(app2)

# Leave gap in the log
Logger.instance.log_chapter("STARTING SIMULATION")

env.run(until=12)