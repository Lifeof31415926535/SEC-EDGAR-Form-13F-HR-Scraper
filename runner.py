#!/usr/bin/env python

import sys


def main():
    from src.cli.command_executors import execute_command
    execute_command(argv=sys.argv)


if __name__ == '__main__':
    main()
