from pathlib import Path
import matplotlib.pyplot as plt
import os
import misc

PLOTS = os.path.join("..", "plots")

def save(file, format=None):
    path = os.path.join(PLOTS, file)
    misc.prep_paths(path)
    plt.savefig(path, format=format, bbox_inches='tight')
    plt.close()

def plot_availability(availability):
    _, ax = plt.subplots()
    x = list()
    y = list() 
    for (t, a) in availability:
        x.append(t)
        y.append(a)
    ax.plot(x, y)
    save("availability.png")