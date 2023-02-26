import src.cli.base as base


class CommandRegistryError(Exception):
    pass


COMMAND_REGISTRY = {}


def register(command_class):
    if not issubclass(command_class, base.Command):
        raise CommandRegistryError("Only a subclass of the 'Command' class can be added to the command registry.")
    COMMAND_REGISTRY[command_class.command_name] = command_class
    return command_class
