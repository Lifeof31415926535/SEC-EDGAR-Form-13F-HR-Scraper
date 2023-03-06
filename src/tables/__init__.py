from .table_managers import PostgresTableManager
from .table_readers import TableReaderFactory
from .table_writers import TableWriterFactory
from config import TABLE_MANAGER_CONFIG
from downloaders import DownloaderFactory
from index_sources import IndexSourceReaderFactory


class TableManagerFactory:
    def __call__(self, config: dict = TABLE_MANAGER_CONFIG):
        manager_type = config.get('type', 'default')
        downloader = config.get('downloader', 'default')
        source_reader = config.get('source', {'reader': 'default', 'batch_size': 20, 'period': {'date': '2022-01-03'}})
        table_reader = config.get('table_reader', 'default')
        table_writer = config.get('table_writer', 'default')

        match manager_type:
            case 'default' | 'Default' | 'postgres' | 'Postgres':
                downloader_factory = DownloaderFactory()
                source_reader_factory = IndexSourceReaderFactory()
                table_reader_factory = TableReaderFactory()
                table_writer_factory = TableWriterFactory()
                return PostgresTableManager(
                    downloader=downloader_factory(downloader),
                    source_reader=source_reader_factory(
                        source_reader['reader'],
                        source_reader['batch_size'],
                        **source_reader['period']
                    ),
                    table_reader=table_reader_factory(table_reader),
                    table_writer=table_writer_factory(table_writer)
                )
