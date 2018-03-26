

from operator import itemgetter
from grasp import cli
from grasp import routines


if __name__ == "__main__":

    args = cli.parse_args(__doc__)

    if args.command == 'infos':
        infos = routines.info(args.infile, args.motifs, args.no_cc,
                              graphics=args.graphics, outdir=args.outdir,
                              heavy_computations=args.heavy_computations,
                              graph_properties=args.graph_properties,
                              round_float=args.round_float,
                              negative_results=args.negative_results,
                              edge_predicate=args.edge_predicate)
        print('\n'.join(infos))
    elif args.command == 'split':
        if args.biggest_first:
            order = 'biggest first'
        elif args.biggest_last:
            order = 'biggest last'
        else:
            order = None
        print(routines.split_by_cc(args.infile, args.targets, order=order,
                                   slice=args.slice,
                                   edge_predicate=args.edge_predicate))
    elif args.command == 'convert':
        routines.convert(args.infile, args.target,
                         anonymize=args.anonymize,
                         edge_predicate=args.edge_predicate,
                         target_edge_predicate=args.target_edge_predicate)
    elif args.command == 'generate':
        routines.generate(target=args.outfile, method=args.method,
                          method_parameters=args.args,
                          edge_predicate=args.edge_predicate)
    else:
        print('WOOT', args)
