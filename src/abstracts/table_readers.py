from abc import ABC, abstractmethod

from src.data.filing_data import FilingData


class TableReader(ABC):
    @abstractmethod
    def read(self, data) -> FilingData:
        pass
