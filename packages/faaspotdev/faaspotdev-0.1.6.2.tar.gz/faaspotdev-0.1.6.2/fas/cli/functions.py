#!/usr/bin/env python
import os
import codecs


def is_valid_file(parser, file_path):
    if not os.path.exists(file_path):
        parser.error("The file `{0}` does not exist!".format(file_path))
    else:
        return codecs.open(file_path, 'r', encoding='utf-8')


def add_functions_args(subparsers):
    root_parser_name = 'functions'
    parser_functions = subparsers.add_parser('functions', help='Manages functions')
    functions = parser_functions.add_subparsers(help='Manage functions',  dest=root_parser_name)

    functions.add_parser('list', help='List functions')

    get = functions.add_parser('get', help='Get a function')
    get.add_argument('function_id',
                     action="store",
                     help='The function-id')
    # When using the cli, call the `get` command with pretty_print argument
    get.set_defaults(pretty_print=True)

    create = functions.add_parser('create', help='Create a new function')
    create.add_argument('name',
                        action="store",
                        help='The name of the function')
    create.add_argument('--file',
                        type=lambda x: is_valid_file(create, x),
                        help='The file code',
                        required=True)
    create.add_argument('-r', '--runtime',
                        help='The runtime executor',
                        dest="runtime",
                        required=True)
    create.add_argument('-c', '--context-file',
                        type=lambda x: is_valid_file(create, x),
                        help='The context file',
                        dest="context_file",
                        required=False)
    create.add_argument('--public',
                        action='store_true',
                        help='Allow execution without a token')
    create.add_argument('--wait',
                        action='store_true',
                        help='Wait for creation')

    update = functions.add_parser('update', help='Update an existing function')
    update.add_argument('name',
                        action="store",
                        help='The name of the function')
    update.add_argument('-f', '--file',
                        type=lambda x: is_valid_file(update, x),
                        help='The code file',
                        dest="file_obj",
                        required=False)
    update.add_argument('-c', '--context-file',
                        type=lambda x: is_valid_file(update, x),
                        help='The context file',
                        dest="context_file",
                        required=False)
    update.add_argument('-n', '--new-name',
                        action="store",
                        dest="new_name",
                        help='New name for the function')
    update.add_argument('-w', '--wait',
                        action='store_true',
                        help='Wait for completion')

    delete = functions.add_parser('delete', help='Delete a function')
    delete.add_argument('name',
                        action="store",
                        help='The function name to delete')
    delete.add_argument('-w', '--wait',
                        action='store_true',
                        help='Wait for creation')

    run = functions.add_parser('run', help='Run an existing function')
    run.add_argument('name',
                     action="store",
                     help='The name of the function')
    run.add_argument('-p', '--parameters',
                     action="append",
                     help='Function parameters, list of key=value',
                     nargs='*',
                     required=False)
    run.add_argument('-w', '--wait',
                     action='store_true',
                     help='Wait for completion')

    run_bulk = functions.add_parser('run_bulk', help='Run bulk of existing function')
    run_bulk.add_argument('name',
                          action="store",
                          help='The name of the function')
    run_bulk.add_argument('-p', '--parameters',
                          action="append",
                          help='Function parameters, list of key=value',
                          nargs='*',
                          required=False)

    samples = functions.add_parser('samples', help='Create a sample function')
    samples_options = samples.add_mutually_exclusive_group()
    samples_options.add_argument('--hello-world',
                                 action="store_true",
                                 help='Generate hello-world function')
    samples_options.add_argument('--get-content',
                                 action="store_true",
                                 help='Generate get-content function')
    samples_options.add_argument('--sleep',
                                 action="store_true",
                                 help='Generate sleep function')
    return root_parser_name
