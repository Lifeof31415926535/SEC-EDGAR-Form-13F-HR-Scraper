import argparse

from .register import COMMAND_REGISTRY


class InvalidCommand(Exception):
    pass


def execute_command(argv):
    command_name = argv[1]
    command_class = COMMAND_REGISTRY.get(command_name)

    if command_class is None:
        raise InvalidCommand(f"No command named '{command_name}' exists.")

    command = command_class()
    command.execute(argv[2:])
