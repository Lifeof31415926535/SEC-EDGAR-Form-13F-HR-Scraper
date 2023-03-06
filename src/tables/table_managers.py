from .table_readers import TableReaderFactory
from .table_writers import TableWriterFactory
from abstracts import TableManager
from downloaders import DownloaderFactory
from config import FILINGS_URL
from index_sources import IndexSourceReaderFactory
from http_modules import Header, Request


class PostgresTableManager(TableManager):
    def _process_source(self, source):
        self._filing_count += 1
        url = f"{FILINGS_URL}{source.file_name}"
        request = Request(header=Header(), url=url)
        response = self.downloader.download(request, max_retries=2)
        if response.errors:
            self._errors.append(response.errors)
            return
        filing = self.table_reader.read(response.data)
        if filing.filing_errors:
            self._errors.append(filing.errors)
            return
        self.table_writer.write(filing, source.id)

    def _process_batch(self, batch):
        for source in batch:
            self._process_source(source)

    def run(self):
        for batch in self.source_reader:
            self._process_batch(batch)

    def print_stats(self):
        failed = len(self._errors)
        successful = self._filing_count - failed
        print(f"Total Filings: {self._filing_count}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print("Dumping errors:")
        for err in self._errors:
            print(err)
