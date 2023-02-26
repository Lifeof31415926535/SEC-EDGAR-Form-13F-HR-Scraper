from abc import ABC, abstractmethod


class IndexFileReader(ABC):
    index_type: str

    @abstractmethod
    def read(self, index_data) -> list[str]:
        pass



