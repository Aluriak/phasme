
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
    parser_clean = subs.add_parser('clean', description='Rewrite file in clean format.')

    give_common_args(parser_infos)
    give_common_args(parser_split)
    give_common_args(parser_clean)

    # infos on graph
    parser_infos.add_argument('--no-cc', action='store_false',
                              help="Do not search for connected components info.")
    parser_infos.add_argument('--motifs', action='store_true',
                              help="Search for bigger motifs stats.")

    # split by cc
    parser_split.add_argument('targets', type=str, default=None,
                              help='file template to write the components in.')
    # clean file

    return parser


def give_common_args(parser):
    parser.add_argument('infile', type=existant_file,
                        help='file containing the graph data.')
    parser.add_argument('--edge-predicate', type=str, default='edge',
                        help='ASP predicate encoding the graph edges.')
