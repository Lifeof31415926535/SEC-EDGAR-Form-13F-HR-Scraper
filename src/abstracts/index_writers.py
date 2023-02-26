from abc import ABC, abstractmethod


class IndexWriter(ABC):
    index_type: str

    @abstractmethod
    def write(self, sources):
        pass
