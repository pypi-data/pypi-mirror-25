# -*- coding: utf-8 -*-

import sys
import ast
import importlib

from iftttcml import buildparser
# from iftttcml.events import people_in_space


def main():
    """Run the command-line interface."""

    parser = buildparser.build_parser()
    options = parser.parse_args()
    params = dict()

    if options.key is None:
        print("Error: Must provide IFTTT secret key.")
        sys.exit(1)

    if options.params:
        params = ast.literal_eval(options.params)

    if options.event:
        mod = importlib.import_module('iftttcml.events.' + options.event)
        mod.launch(options.key, options.event, params)


if __name__ == '__main__':
    main()
