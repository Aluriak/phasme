

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
                              edge_predicate=args.edge_predicate)
        for field, value in infos:
            value = ', '.join(map(str, value)) if isinstance(value, (tuple, list, set)) else str(value)
            print(field.rjust(22) + ' | ' + value)
    elif args.command == 'split':
        print(routines.split_by_cc(args.infile, args.targets,
                                   edge_predicate=args.edge_predicate))
    elif args.command == 'clean':
        routines.clean(args.infile, args.target,
                       edge_predicate=args.edge_predicate,
                       target_edge_predicate=args.target_edge_predicate)
    else:
        print('WOOT', args)
