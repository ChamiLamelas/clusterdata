import matplotlib.pyplot as plt
import os
import misc

PLOTS = os.path.join("..", "plots")

def save(file, format=None):
    path = os.path.join(PLOTS, file)
    misc.prep_paths(path)
    plt.savefig(path, format=format, bbox_inches='tight')
    plt.close()

def make_plot_nice(ax, xlabel, ylabel, ymin, ymax, xmin=None, xmax=None, fontsize=16, legendcol=None):
    if legendcol is not None:
        ax.legend(fontsize=fontsize, ncol=legendcol, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params('y', labelsize=fontsize)
    ax.tick_params('x', labelsize=fontsize)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.set_ylim([ymin, ymax])
    if xmin is not None and xmax is not None:
        ax.set_xlim([xmin, xmax])
    ax.grid()

def plot_availability(availability):
    _, ax = plt.subplots()
    x = list()
    y = list() 
    for (t, a) in availability:
        x.append(t / 3600)
        y.append(a)
    ax.plot(x, y)
    make_plot_nice(ax, 'time (hr)', '# GPUs', 5200, 6800, xmin=0, xmax=2000)
    save("availability.png")