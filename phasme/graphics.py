import matplotlib.pyplot as plt
import networkx as nx
import os

def make_all(graph, outdir):
    make_degree_distrib(graph, outdir)

def make_degree_distrib(graph, outdir, bins: int = 100, no_one: bool = False, log: bool = False):
    """Create a distribution histogram of the degrees"""
    degrees = list(graph.degree().values())

    color = "green"
    title = "Degree distribution"
    data_list = degrees[:]
    # remove the values equal to 1
    if no_one:
        data_list = [x for x in data_list if x != 1]
        title += " - without degree = 1"
    # number of bars
    num_bins = bins
    x = data_list
    plt.hist(x, num_bins, edgecolor='black', facecolor=color, alpha=0.5)

    # log scale
    if log:
        plt.yscale('log')
        title += " - log scale"
    plt.xlabel("Degree")
    plt.ylabel("Count")
    plt.title(title)
    plt.grid(True)

    # choose file name
    i = 1
    file_name = "{}degree_distrib.png".format(outdir)
    while os.path.exists(file_name):
        file_name = "{}degree_distrib_{}.png".format(outdir, i)
        i += 1

    plt.savefig(file_name)
