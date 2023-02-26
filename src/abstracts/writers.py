from abc import ABC, abstractmethod

from src.data.filing_data import FilingData


class TableWriter(ABC):
    @abstractmethod
    def write(self, data: FilingData):
        pass
