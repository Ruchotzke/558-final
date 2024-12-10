import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.figure(figsize=(5, 5),dpi=300)

info = [('s1_1.txt','green','flow 1'),('s1_2.txt','orange','flow 2'),('s1_3.txt','blue','flow 3')]

for i in info:
    # Open the file and read the info out
    target = os.path.join("..", "..", "runs", "rr_excess", i[0])
    data = pd.read_csv(target,names=['arrival','length','sent','id'])

    # Compute each packet's latency
    latency = data['arrival'].to_numpy() - data['sent'].to_numpy()
    print(latency)

    # Plot the latency
    plt.scatter(data['arrival'].to_numpy(), latency, s=10, label=i[2], color=i[1])

plt.title("Round Robin Latency - Excess")
plt.xlabel("Arrival time (s)")
plt.ylabel("Packet Latency (s)")
plt.legend()
plt.show()