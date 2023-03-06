from abstracts import *
from periods import FilingPeriod, filing_quarter
from typing import Tuple

from config import INDEX_URL, DEFAULT_BATCH_SIZE, FILINGS_URL, INDEX_SCRAPER_CONFIG
from index_sources import IndexFileManagerFactory
from tables import TableManagerFactory


class IndexScraper:
    def __init__(
            self,
            period: FilingPeriod,
            manager_config: dict = INDEX_SCRAPER_CONFIG
    ):
        self.period = period
        index_file_manager_factory = IndexFileManagerFactory()
        self.manager = index_file_manager_factory(**manager_config)

    def start(self):
        self._controller()
        self._print_stats()

    def _controller(self):
        index_type = self.manager.index_type
        for date in self.period.dates:
            url = f"{INDEX_URL}{date.year}/{date.quarter_str}/{index_type}.{date.date_str}.idx"
            self.manager.run(url)

    def _print_stats(self):
        print(f"Successful: {self.manager.successful}")
        print(f"Failed: {self.manager.failed}")
        if self.manager.errors:
            print('Dumping errors.')
            for error in self.manager.errors:
                print(error)


class TableScraper:
    def __init__(self, manager_factory=TableManagerFactory()):
        self.manager = manager_factory()

    def start(self):
        self._controller()

    def _controller(self):
        self.manager.run()
        self.manager.print_stats()


if __name__ == '__main__':
    ts = TableScraper()
    ts.start()
