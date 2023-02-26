from abstracts import *
from periods import FilingPeriod
from typing import Tuple

from config import INDEX_URL, DEFAULT_BATCH_SIZE, FILINGS_URL
from http_modules.requests import Header, Request


class IndexScraper:
    def __init__(
            self,
            period: FilingPeriod,
            downloader: Downloader,
            index_reader: IndexFileReader,
            index_writer: IndexWriter,
    ):
        self.period = period
        self.downloader = downloader
        self.index_reader = index_reader
        self.index_writer = index_writer

    def start(self):
        self._controller()

    def _controller(self):
        header = Header()
        index_type = self.index_reader.index_type
        for date in self.period.dates:
            url = f"{INDEX_URL}{date.year}/{date.quarter_str}/{index_type}.{date.date_str}.idx"
            request = Request(
                header=header,
                url=url
            )

            response = self.downloader.download(request, max_retries=3)

            if response.status != 200:
                continue

            sources = self.index_reader.read(response.data)
            self.index_writer.write(sources)


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

