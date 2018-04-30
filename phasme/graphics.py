"""Module containing general routines for graphics generation using matplotlib.

Used by routines to produce loads of visualizations.

"""
import inspect
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os


def make_all(graph, outdir:str, params:dict=None):
    """
    Make all the graphs, yield the outfiles name and their description.
    params = {arg: value}
    """
    if params is None:
        params = {}
    get_description = lambda f: f.__doc__.splitlines(False)[0]
    get_args = lambda f: inspect.getfullargspec(f).args

    # list containing the graphics functions
    func_list = [v for k, v in globals().items() if k.startswith("make_graphics")]

    for func in func_list:
        func_params = get_args(func)
        outfile = func(graph, outdir, **{p: v for p, v in params.items() if p in func_params})
        yield outfile, get_description(func)


def choose_name(outdir, file_name:str):
    idx = 1
    file_path = '{}/{}.png'.format(outdir, file_name)
    while os.path.exists(file_path):
        file_path = '{}/{}_{}.png'.format(outdir, file_name, idx)
        idx += 1
    return file_path


def make_graphics_degree(graph, outdir:str, bins:int=50, no_one:bool=False, logxscale:bool=False,
                         logyscale:bool=False, degree_color:str='green'):
    """degree distribution histogram"""
    degrees = [deg for _, deg in graph.degree()]

    title = "Degree distribution"
    # remove the values equal to 1
    if no_one:
        data_list = [x for x in degrees if x != 1]
        title += " - without degree = 1"
    else:
        data_list = list(degrees)
    # number of bars
    num_bins = bins
    x = data_list
    plt.hist(x, num_bins, edgecolor='black', facecolor=degree_color, alpha=0.8)

    xlabel = "Degree"
    ylabel = "Count"

    # log scale
    if logxscale or logyscale:
        title += " - log scale"
        if logxscale:
            plt.xscale('log')
            xlabel += " (log)"
        if logyscale:
            plt.yscale('log')
            ylabel += " (log)"

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

    # choose file name
    outfile_path = choose_name(outdir, "degree_distrib")

    plt.savefig(outfile_path)
    # clear the current figure
    plt.clf()
    file_name = os.path.basename(outfile_path)
    return file_name


def make_graphics_coef(graph, outdir:str, bins:int=50, no_zero:bool=False,
                       logxscale:bool=False, logyscale:bool=False, coef_color:str='blue'):
    """clustering coefficient distribution histogram"""
    coefs = list(nx.clustering(graph).values())

    title = "Coef distribution"
    data_list = coefs[:]
    # remove the values equal to 0
    if no_zero:
        data_list = [x for x in data_list if x != 0]
        title += " - without zero"
    # number of bars
    num_bins = bins
    x = data_list
    plt.hist(x, num_bins, edgecolor='black', facecolor=coef_color, alpha=0.8)

    xlabel = "Coef"
    ylabel = "Count"

    # log scale
    if logxscale or logyscale:
        title += " - log scale"
        if logxscale:
            plt.xscale('log')
            xlabel += " (log)"
        if logyscale:
            plt.yscale('log')
            ylabel += " (log)"

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)

    # choose file name
    outfile_path = choose_name(outdir, "coef_distrib")

    plt.savefig(outfile_path)
    # clear the current figure
    plt.clf()
    file_name = os.path.basename(outfile_path)
    return file_name


def make_graphics_coef_stacked(graph, outdir:str, bins:int=50, no_zero:bool=False,
                               logxscale:bool=False, logyscale:bool=False, stacked_limits:list=None,
                               stacked_colors:list=None):
    """clustering coefficient distribution histogram with different degree categories
    Create a distribution histogram of the local clustering coefficients.
    By default, 4 colors for each bar:
        - green: degree <= 4
        - yellow/green: 4 < degree <= 10
        - yellow: 10 < degree <= 30
        - red: degree > 30
    """
    # default colors and the different thresholds
    if stacked_limits is None:
        stacked_limits = [4, 10, 30]
    if stacked_colors is None:
        stacked_colors = ['mediumseagreen', 'greenyellow', 'gold', 'orangered']
    # TODO define a default color list depending on the threshold list length, ex: default gradient
    assert len(stacked_colors) == len(stacked_limits) + 1, "Colors length must be equal to Limits" \
                                                           " length + 1"

    degrees = graph.degree()
    coefs = nx.clustering(graph)

    title = "Local clustering coefficient distribution with degree"

    x = []
    for i in range(len(stacked_limits) + 1):
        # retrieve the nodes for each degree category
        # first value
        if i == 0:
            node_degree = {k: v for (k, v) in degrees if v <= stacked_limits[i]}
        # last value
        elif i == len(stacked_limits):
            node_degree = {k: v for (k, v) in degrees if v > stacked_limits[i - 1]}
        else:
            node_degree = {k: v for (k, v) in degrees if stacked_limits[i - 1] <= v <=
                           stacked_limits[i]}
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
    for i in range(len(stacked_limits)):
        labels.append("degree <= {}".format(stacked_limits[i]))
    # add last legend item
    labels.append("degree > {}".format(stacked_limits[-1]))

    num_bins = bins
    plt.hist(x, num_bins, edgecolor='black', histtype='bar', stacked=True, color=stacked_colors,
             label=labels, alpha=0.8)

    # change axis length
    ymax = plt.gca().get_ybound()
    ymax = ymax[1] * 1.1
    xmax = plt.gca().get_xbound()[1]
    plt.axis([0, xmax, 0, ymax])

    xlabel = "Coef"
    ylabel = "Count"

    # log scale
    if logxscale or logyscale:
        title += " - log scale"
        if logxscale:
            plt.xscale('log')
            xlabel += " (log)"
        if logyscale:
            plt.yscale('log')
            ylabel += " (log)"

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(prop={'size': 10})
    plt.grid(True)

    # choose file name
    outfile_path = choose_name(outdir, "coef_distrib_stacked")

    plt.savefig(outfile_path)
    # clear the current figure
    plt.clf()
    file_name = os.path.basename(outfile_path)
    return file_name
