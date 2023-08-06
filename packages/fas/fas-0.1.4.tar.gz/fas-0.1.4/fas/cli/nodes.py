#!/usr/bin/env python


def add_nodes_args(subparsers):
    root_parser_name = 'nodes'
    parser_nodes = subparsers.add_parser('nodes', help='Manages nodes')
    nodes = parser_nodes.add_subparsers(help='Manage nodes',
                                        dest=root_parser_name)

    nodes.add_parser('list', help='List nodes')

    add = nodes.add_parser('add',
                           help='Increase the number of nodes by one')
    add.add_argument('-w', '--wait',
                     action='store_true',
                     help='Wait for creation')

    get = nodes.add_parser('get', help='Get status on a node')
    get.add_argument('ip',
                     action="store",
                     help='Specify node ip to delete')

    remove = nodes.add_parser('remove',
                              help='Reduce the number of nodes by one')
    remove.add_argument('-i', '--ip',
                        action="store",
                        help='Specify which node to remove')
    remove.add_argument('-w', '--wait',
                        action='store_true',
                        help='Wait for deletion')

    update = nodes.add_parser('update', help='Update node parameters')
    update.add_argument('--min',
                        action="store",
                        help='Specify minimum amount of workers in a node')
    update.add_argument('--max',
                        action="store",
                        help='Specify maximum amount of workers in a node')

    refresh_ip = nodes.add_parser('refresh_ip', help='Refresh node instances ip')
    refresh_ip.add_argument('-w', '--wait',
                            action='store_true',
                            help='Wait for task completion')
    refresh_ip.add_argument('-i', '--ip',
                            action="store",
                            help='Specify which node ip to refresh')

    replace = nodes.add_parser('replace',
                               help='Remove node and create another one instead')
    replace.add_argument('ip',
                         action="store",
                         help='Specify which node to replace')

    return root_parser_name
