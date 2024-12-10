#Imports
import matplotlib.pyplot as plt
import numpy as np

# Example data
algorithms = ['FIFO', 'Round Robin', 'Fair Queue']
results = np.array([
    [25000, 24980, 25000],
    [23600, 4780, 46800],
    [25000, 24980, 25000],
])

# Bar settings
num_algorithms = len(algorithms)
num_results = results.shape[1]
x_positions = np.arange(num_algorithms)  # Base positions for each algorithm
bar_width = 0.25  # Width of each bar

# Adjust positions for each result group
positions = [x_positions + i * bar_width - (bar_width * (num_results - 1) / 2) for i in range(num_results)]

# Plot bars for each result
colors = ['skyblue', 'lightgreen', 'salmon']
flows = ['flow 1', 'flow 2', 'flow 3']
for i in range(num_results):
    plt.bar(positions[i], results[:, i], width=bar_width, label=flows[i], color=colors[i])

# Add labels, legend, and title
plt.xticks(x_positions, algorithms)  # Center ticks for algorithms
plt.xlabel('Queueing Algorithm')
plt.ylabel('Bytes received')
plt.title('Queueing Algorithm Performance')
plt.legend()

# Show the plot
plt.show()