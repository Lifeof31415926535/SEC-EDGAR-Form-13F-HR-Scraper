from abc import ABC, abstractmethod


class SourceReader(ABC):
    def __init__(self, batch_size):
        self._sources = []
        self._current = 0
        self._batch_size = batch_size
        self._initialize()

    def __iter__(self):
        batch = self.next_batch()
        while batch is not None:
            yield batch
            batch = self.next_batch()

    @abstractmethod
    def _initialize(self):
        pass

    def next_batch(self) -> list | None:
        if self._current >= len(self._sources):
            return
        next_idx = self._current + self._batch_size
        batch = self._sources[self._current: next_idx]
        self._current = next_idx
        return batch
