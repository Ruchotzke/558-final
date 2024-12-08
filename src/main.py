import simpy

from Node import Node
from Network import Network

env = simpy.Environment()

N1 = Node(env, "N1")
N2 = Node(env, "N2")
net = Network(env)

N1.add_interface(net, "", "")
N2.add_interface(net, "", "")

N1.start_process()
N2.start_process()

env.run(until=15)