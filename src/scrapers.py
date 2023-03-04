from abstracts import *
from periods import FilingPeriod, filing_quarter
from typing import Tuple

from config import INDEX_URL, DEFAULT_BATCH_SIZE, FILINGS_URL, INDEX_SCRAPER_CONFIG
from index_sources import IndexFileManagerFactory


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


"""
class TableScraper:
    def __init__(
            self,
            downloader: Downloader,
            source_reader: SourceReader,
            table_reader: TableReader,
            writer: TableWriter,
    ):
        self.downloader = downloader
        self.source_reader = source_reader
        self.table_reader = table_reader
        self.writer = writer

    def start(self, start_date: Tuple[int, int, int], end_date: Tuple[int, int, int], batch_size=DEFAULT_BATCH_SIZE):
        self._controller(start_date, end_date, batch_size)

    def _controller(self, start_date: Tuple[int, int, int], end_date: Tuple[int, int, int], batch_size: int):
        self.source_reader.initialize(start_date, end_date, batch_size)
        header = Header()
        filing_batch = self.source_reader.next_batch()

        while filing_batch is not None:
            for source in filing_batch:
                url = f"{FILINGS_URL}{source.url_path}"
                request = Request(header=header, url=url)
                response = self.downloader.download(request, max_retries=3)

                if response.status != 200:
                    continue

                filing = self.table_reader.read(response.data)
                self.writer.write(filing)
"""

if __name__ == '__main__':
    filing_period = filing_quarter(2022, 1)
    index_scraper = IndexScraper(period=filing_period)
    index_scraper.start()

