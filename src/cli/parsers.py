import re

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable


@dataclass
class ParserOption:
    flag: str
    long_flag: str
    values: list | tuple
    default_value: Any = field(default=None)
    help_str: str = field(default=None)


@dataclass
class ParserOptionInstance:
    argument: Any
    option: ParserOption

    def __post_init__(self):
        print(self.option.values)
        if self.argument not in self.option.values:
            raise Exception("")


class Parser:
    def __init__(self, argv: list[str], options: list[ParserOption]):
        self.argv = argv
        self.options = options
        self._map_options()

    def _map_options(self):
        self._option_flag_map = {}
        self._option_long_flag_map = {}

        for opt in self.options:
            self._option_flag_map[opt.flag] = opt
            self._option_long_flag_map[opt.long_flag] = opt

    def parse(self) -> list[ParserOptionInstance]:
        option_list = []

        regex = '-{1,2}.*'

        for arg in self.argv:
            if re.match(regex, arg) is not None:
                index = self.argv.index(arg)
                if index > len(self.argv) - 1 or re.match(regex, self.argv[index + 1]):
                    raise Exception("")
                opt = self._option_flag_map.get(arg[1:])
                if opt is not None:
                    value = self.argv[index + 1]
                    option_list.append(
                        ParserOptionInstance(
                            option=opt,
                            argument=value
                        )
                    )

                    continue
                opt = self._option_long_flag_map.get(arg[2:])
                if opt is not None:
                    value = self.argv[index + 1]
                    option_list.append(
                        ParserOptionInstance(
                            option=opt,
                            argument=value
                        )
                    )
                    self._option_flag_map.pop(opt.flag)
                    self._option_long_flag_map.pop(opt.long_flag)

        assert len(self._option_flag_map) == len(self._option_long_flag_map)

        for flag, option in self._option_flag_map.items():
            if option.default_value is not None:
                option_list.append(
                    ParserOptionInstance(
                        option=option,
                        argument=option.default_value
                    )
                )

        return option_list
