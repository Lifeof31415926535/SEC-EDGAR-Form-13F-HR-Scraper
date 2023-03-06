from abc import ABC, abstractmethod


class TableManager(ABC):

    def __init__(
            self,
            downloader,
            source_reader,
            table_reader,
            table_writer
    ):
        self.downloader = downloader
        self.source_reader = source_reader
        self.table_reader = table_reader
        self.table_writer = table_writer
        self._errors = []
        self._filing_count = 0

    @classmethod
    def set_factories(
            cls,
            downloader_factory,
            source_reader_factory,
            reader_factory,
            writer_factory,
    ):
        cls.downloader_factory = downloader_factory
        cls.source_reader_factory = source_reader_factory
        cls.reader_factory = reader_factory
        cls.writer_factory = writer_factory

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def print_stats(self):
        pass
