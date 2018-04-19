"""Module containing general routines for graphics generation using pandas/matplotlib.

Used by routines to produce loads of visualizations.

"""
import inspect
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os


def make_all(graph, outdir: str, params: dict = None):
    """
    Make all the graphs, yield the outfile name and its description.
    params = {arg: value}
    """
    get_description = lambda f: f.__doc__.splitlines(False)[0]
    get_args = lambda f: inspect.getfullargspec(f)[0]

    # list containing the graphics functions
    func_list = [v for k, v in globals().items() if k.startswith("make_graphics")]

    for func in func_list:
        func_params = get_args(func)
        outfile = func(graph, outdir, **{p: v for p, v in params.items() if p in func_params})
        yield outfile, get_description(func)

    ...  # more functions to call


def make_graphics_degree(graph, outdir: str, bins: int = 50, no_one: bool = False,
                         log: bool = False, degree_color: str = 'green'):
    """degree distribution histogram"""
    degrees = list(graph.degree().values())

    title = "Degree distribution"
    data_list = degrees[:]
    # remove the values equal to 1
    if no_one:
        data_list = [x for x in data_list if x != 1]
        title += " - without degree = 1"
    # number of bars
    num_bins = bins
    x = data_list
    plt.hist(x, num_bins, edgecolor='black', facecolor=degree_color, alpha=0.8)

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
    file_name = "{}/degree_distrib.png".format(outdir)
    while os.path.exists(file_name):
        file_name = "{}/degree_distrib_{}.png".format(outdir, i)
        i += 1

    plt.savefig(file_name)
    # clear the current figure
    plt.clf()
    file_name = os.path.basename(file_name)
    return file_name


def make_graphics_coef(graph, outdir: str, bins: int = 50, no_zero: bool = False,
                       log: bool = False, coef_color: str = 'blue'):
    """clustering coefficient distribution histogram"""
    coefs = list(nx.clustering(graph).values())

    title = "Coef distribution"
    data_list = coefs[:]
    # remove the values equal to 1
    if no_zero:
        data_list = [x for x in data_list if x != 0]
        title += " - without zero"
    # number of bars
    num_bins = bins
    x = data_list
    plt.hist(x, num_bins, edgecolor='black', facecolor=coef_color, alpha=0.8)

    # log scale
    if log:
        plt.yscale('log')
        title += " - log scale"
    plt.xlabel("Coef")
    plt.ylabel("Count")
    plt.title(title)
    plt.grid(True)

    # choose file name
    i = 1
    file_name = "{}/coef_distrib.png".format(outdir)
    while os.path.exists(file_name):
        file_name = "{}/coef_distrib_{}.png".format(outdir, i)
        i += 1

    plt.savefig(file_name)
    # clear the current figure
    plt.clf()
    file_name = os.path.basename(file_name)
    return file_name


# TODO add parameters to choose the threshold values + colors
def make_graphics_coef_stacked(graph, outdir: str, bins: int = 50, no_zero: bool = False,
                               log: bool = False):
    """clustering coefficient distribution histogram with different degree categories
    Create a distribution histogram of the local clustering coefficients.
    4 colors for each bar, ex:
        - green: degree <= 4
        - yellow/green: 4 < degree <= 10
        - yellow: 10 < degree <= 30
        - red: degree > 30
    """
    degrees = graph.degree()
    coefs = nx.clustering(graph)

    title = "Local clustering coefficient distribution with degree"

    # choose the colors and the different thresholds
    limit_list = [4, 10, 30]
    colors = ['mediumseagreen', 'greenyellow', 'gold', 'orangered']
    assert len(colors) == len(limit_list) + 1, "Colors length is not ok"

    x = []
    for i in range(len(limit_list) + 1):
        # retrieve the nodes for each degree category
        # first value
        if i == 0:
            node_degree = {k: v for (k, v) in degrees.items() if v <= limit_list[i]}
        # last value
        elif i == len(limit_list):
            node_degree = {k: v for (k, v) in degrees.items() if v > limit_list[i - 1]}
        else:
            node_degree = {k: v for (k, v) in degrees.items() if limit_list[i - 1] <= v <=
                           limit_list[i]}
        # retrieve the coef for the selected nodes
        node_coef = {k: v for (k, v) in coefs.items() if k in node_degree}
        # retrieve the list of values from node_coef
        values = list(node_coef.values())
        if no_zero:
            values[:] = [x for x in values if x != 0]
        # array w/ 1 column
        values = np.transpose(np.array([values]))
        x.append(values)
    if no_zero:
        title += " - without zero"

    # set the legend
    labels = []
    for i in range(len(limit_list)):
        labels.append("degree <= {}".format(limit_list[i]))
    # add last legend item
    labels.append("degree > {}".format(limit_list[-1]))

    num_bins = bins
    plt.hist(x, num_bins, edgecolor='black', histtype='bar', stacked=True, color=colors,
             label=labels, alpha=0.8)

    # change axis length
    ymax = plt.gca().get_ybound()
    ymax = ymax[1] * 1.1
    xmax = plt.gca().get_xbound()[1]
    plt.axis([0, xmax, 0, ymax])

    # log scale
    if log:
        plt.yscale('log')
        title += " - log scale"

    # axis labels and title
    plt.xlabel("Coef")
    plt.ylabel("Count")
    plt.title(title)
    plt.legend(prop={'size': 10})
    plt.grid(True)

    # choose file name
    i = 1
    file_name = "{}/coef_distrib_stacked.png".format(outdir)
    while os.path.exists(file_name):
        file_name = "{}/coef_distrib_stacked_{}.png".format(outdir, i)
        i += 1

    plt.savefig(file_name)
    # clear the current figure
    plt.clf()
    file_name = os.path.basename(file_name)
    return file_name
