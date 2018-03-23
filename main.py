

import cli
import routines
from operator import itemgetter


if __name__ == "__main__":
    args = cli.parse_args(__doc__)

    if args.command == 'infos':
        infos = routines.info(args.infile, args.motifs, args.no_cc,
                              edge_predicate=args.edge_predicate)
        for field, value in infos:
            value = ', '.join(map(str, value)) if isinstance(value, (tuple, list, set)) else str(value)
            print(field.rjust(20) + ' | ' + value)
    elif args.command == 'split':
        print(routines.split_by_cc(args.infile, args.targets,
                                   edge_predicate=args.edge_predicate))
    elif args.command == 'clean':
        print(routines.clean(args.infile, args.target))
    else:
        print('WOOT', args)
