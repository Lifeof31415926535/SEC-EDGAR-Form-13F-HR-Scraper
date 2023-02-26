from typing import Type


def are_instances(__type: Type, *objects):
    return all([isinstance(obj, __type) for obj in objects])
