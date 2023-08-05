import sys
import purchases


def analytics(command, arg_parser):
    command
    files = sys.argv[2:]
    if command == 'an_purchases':
        purchases.main(files)
