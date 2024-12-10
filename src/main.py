import os.path

import simpy

from src.components.Node import Node
from src.components.Network import Network
from src.components.addressing.EthernetAddr import EthernetAddr
from src.components.addressing.IPAddr import IPAddr
from src.components.apps.Generator import GeneratorApp
from src.components.apps.Listener import ListenerApp
from src.components.apps.LogServer import LogServerApp
from src.components.disciplines.FQ import FQDiscipline
from src.components.disciplines.RoundRobin import RoundRobinDiscipline
from src.utilities import RouteGenerator
from src.utilities.Logger import Logger, Level

env = simpy.Environment()

# Init the logger
logger = Logger()
logger.init_instance(env)
logger.instance.LOG_LEVEL = Level.ERROR

#
# Network Vision
#
# N1 N2 N3  R1        S1
#  |  |  |  ||        |
#   ========  ========
#    x.x.0.0   x.x.1.0

# Set up simulation logging

# Set up folder for this run
base_folder = "runs/run"
counter = 1
while os.path.exists(f"{base_folder}_{counter}"):
    counter += 1
    folder_name = f"{base_folder}_{counter}"

# Generate folder
base_folder = f"{base_folder}_{counter}"
os.makedirs(base_folder)
Logger.instance.log(Level.INFO, f"Generated run folder {base_folder}")

# Generate left network
N1 = Node(env, "N1")
N2 = Node(env, "N2")
N3 = Node(env, "N3")
left_net = Network(env, IPAddr("192.168.0.0"))
left_net.bandwidth = 5000
env.process(left_net.proc_sample_utilization(os.path.join(base_folder, "left_net")))

N1.add_interface(left_net, EthernetAddr("00:11:11:11:11:11"), IPAddr("192.168.0.1"))
N2.add_interface(left_net, EthernetAddr("00:22:22:22:22:22"), IPAddr("192.168.0.2"))
N3.add_interface(left_net, EthernetAddr("00:33:33:33:33:33"), IPAddr("192.168.0.3"))

# Generate right network
S1 = Node(env, "S1")
S2 = Node(env, "S2")
right_net = Network(env, IPAddr("192.168.1.0"))
right_net.bandwidth = 150
env.process(right_net.proc_sample_utilization(os.path.join(base_folder, "right_net")))


S1.add_interface(right_net, EthernetAddr("11:EE:EE:EE:EE:EE"), IPAddr("192.168.1.1"))
S2.add_interface(right_net, EthernetAddr("11:FF:FF:FF:FF:FF"), IPAddr("192.168.1.2"))

# Generate router discipline
rr = RoundRobinDiscipline(os.path.join(base_folder, "discipline"))
rr.init_flows([IPAddr("192.168.0.1"), IPAddr("192.168.0.2"), IPAddr("192.168.0.3")], False)

# Generate router
R1 = Node(env, "R1")
R1.add_interface(left_net, EthernetAddr("00:44:44:44:44:44"), IPAddr("192.168.0.254"), disc=rr)
R1.add_interface(right_net, EthernetAddr("11:44:44:44:44:44"), IPAddr("192.168.1.254"))
R1.stack.set_router(True)

# Network setup
nets = [left_net, right_net]
RouteGenerator.update_routes(nets)

# Install apps on nodes
app = GeneratorApp(env, N1, IPAddr("192.168.1.1"), 1, 1, 100)
N1.install_app(app)

app = GeneratorApp(env, N2, IPAddr("192.168.1.1"), 50, 0.2, 20)
N2.install_app(app)

app = GeneratorApp(env, N3, IPAddr("192.168.1.1"), 100, 2, 200)
N3.install_app(app)

# Generate log server processes
file = os.path.join(base_folder, "s1_1.txt")
app2 = (LogServerApp(env, S1, 1, file))
S1.install_app(app2)

file = os.path.join(base_folder, "s1_2.txt")
app2 = (LogServerApp(env, S1, 50, file))
S1.install_app(app2)

file = os.path.join(base_folder, "s1_3.txt")
app2 = (LogServerApp(env, S1, 100, file))
S1.install_app(app2)

# Leave gap in the log
Logger.instance.log_chapter("STARTING SIMULATION")

env.run(until=500)