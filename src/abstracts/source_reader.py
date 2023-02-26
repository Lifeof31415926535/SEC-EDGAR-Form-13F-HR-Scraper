from abc import ABC, abstractmethod

from src.data.filining_sources import FilingSource


class SourceReader(ABC):
    @abstractmethod
    def initialize(self, start, end, batch_size: int):
        pass

    @abstractmethod
    def next_batch(self) -> list[FilingSource] | None:
        pass

