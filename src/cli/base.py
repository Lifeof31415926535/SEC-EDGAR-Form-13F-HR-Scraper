from abc import ABC, abstractmethod


class Command(ABC):
    command_name: str

    @abstractmethod
    def execute(self, argv: dict):
        pass
