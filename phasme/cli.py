
import os
import argparse


def parse_args(description:str, args:iter=None) -> dict:
    return cli_parser(description).parse_args(args)

def existant_file(filepath:str) -> str:
    """Argparse type, raising an error if given file does not exists"""
    if not os.path.exists(filepath):
        raise argparse.ArgumentTypeError("file {} doesn't exists".format(filepath))
    return filepath

def writable_file(filepath:str) -> str:
    """Argparse type, raising an error if given file is not writable.
    Will delete the file !

    """
    try:
        with open(filepath, 'w') as fd:
            pass
        os.remove(filepath)
        return filepath
    except (PermissionError, IOError):
        raise argparse.ArgumentTypeError("file {} is not writable.".format(filepath))

def cli_parser(description:str) -> argparse.ArgumentParser:
    # main parser
    parser = argparse.ArgumentParser(description=description)
    subs = parser.add_subparsers(title='command to run', dest='command')

    # subparsers
    parser_infos = subs.add_parser('infos', description='Print general info about the graph.')
    parser_split = subs.add_parser('split', description='Split graph by cc.')
    parser_convr = subs.add_parser('convert', description='Convert, rewrite or anonymize graph to standard format or clean ASP.')
    parser_genrt = subs.add_parser('generate', description='Generate an ASP graph file.')
    parser_extra = subs.add_parser('extract', description='Extract subgraphs.')
    parser_randm = subs.add_parser('randomize', description='Build a randomization.')

    give_common_args(parser_infos)
    give_common_args(parser_split)
    give_common_args(parser_convr)
    give_common_args(parser_genrt, infile_is_outfile=True)
    give_common_args(parser_extra)
    give_common_args(parser_randm)


    # infos on graph
    parser_infos.add_argument('--no-cc', '-nc', action='store_false',
                              help="Do not search for connected components info.")
    parser_infos.add_argument('--motifs', '-m', action='store_true',
                              help="Search for biggest motifs stats.")
    parser_infos.add_argument('--heavy-computations', '-c', action='store_true',
                              help="Perform costly detection of graph features.")
    parser_infos.add_argument('--special-nodes', '-sn', action='store_true',
                              help="Detect and show special nodes.")
    parser_infos.add_argument('--graph-properties', '-p', action='store_true',
                              help="Use networkx to compute graph properties.")
    parser_infos.add_argument('--negative-results', '-nr', action='store_true',
                              help="Show non implemented methods and invalid properties.")
    parser_infos.add_argument('--graphics', '-g', action='store_true',
                              help="Produce and save various graphics and visualizations.")
    parser_infos.add_argument('--outdir', '-o', type=str, default='.',
                              help="Where to put produced files, if any.")
    parser_infos.add_argument('--round-float', '-r', type=int, default=None,
                              help='Round floats with given number of figures after dot.')

    # split by cc
    parser_split.add_argument('targets', type=str, default=None,
                              help='file template to write the components in.')
    parser_split.add_argument('--biggest-first', action='store_true',
                              help='Sort cc by decreasing size.')
    parser_split.add_argument('--biggest-last', action='store_true',
                              help='Sort cc by increasing size.')
    parser_split.add_argument('--slice', type=int, nargs=2, metavar=('FIRST', 'LAST'),
                              default=None, help='Slice to select connected components to extract.')

    # convert, clean or anonymize file
    parser_convr.add_argument('target', type=str, default=None,
                              help='file to write the graph in.')
    parser_convr.add_argument('--target-edge-predicate', type=str, default='edge',
                              help='ASP predicate encoding the graph edges in target.')
    parser_convr.add_argument('--anonymize', action='store_true',
                              help='Rename nodes into integers.')
    parser_convr.add_argument('--normalize', action='store_true',
                              help='Rename nodes with special characters.')

    # generate graph
    parser_genrt.add_argument('method', type=str, help='Generation method.')
    parser_genrt.add_argument('args', type=str, nargs='+', metavar='F=V',
                              default=None, help='Args to give to the generation method.')

    # extract subgraphs from given graph
    parser_extra.add_argument('target', type=str, default=None,
                              help='file to write the subgraph in.')
    parser_extra_subs = parser_extra.add_subparsers(title='extraction method', dest='extraction')
    # extract by giving a list of nodes
    parser_extra_bynode = parser_extra_subs.add_parser(
        'nodes', description="Extract given nodes, and their neighbors."
    )
    parser_extra_bynode.add_argument('nodes', type=str, nargs='+', metavar='NODE',
                                     default=(), help="Nodes to extract.")
    parser_extra_bynode.add_argument('neighbors', type=int, default=1,
                                     help="Extract also neighbors of target of n-th order.")
    parser_extra_bynode.add_argument('--nodes-in-file', '-f', action='store_true',
                                     help="Nodes argument is a file containing the nodes to extract.")

    # parser_extra_motifs = parser_extra_subs.add_parser(
        # 'motif', description="Extract maximal motifs."
    # )

    # build a randomized graph.
    parser_randm.add_argument('target', type=str,
                              help='file to write the generated graph in.')
    parser_randm.add_argument('--iterations', '-i', default=100, type=int,
                              help="Number of iterations divided by number of edges (Q in Milo et al.).")
    parser_randm.add_argument('--per-cc', '-c', action='store_true',
                              help="Run the randomization independantly for each connected component.")
    return parser


def give_common_args(parser, *, infile_is_outfile:bool=False):
    if infile_is_outfile:
        parser.add_argument('outfile', type=writable_file,
                            help='file to write the graph data in.')
    else:
        parser.add_argument('infile', type=existant_file,
                            help='file containing the graph data.')
    parser.add_argument('--edge-predicate', type=str, default='edge',
                        help='ASP predicate encoding the graph edges in fname.')
