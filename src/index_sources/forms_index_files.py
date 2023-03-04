import re
import psycopg2.sql as sql

from abc import ABC
from abstracts import IndexWriter, IndexFileManager, IndexFileReader
from uuid import uuid4

from db import connection_manager
from src.data.index_data import FormIndexData
from downloaders import DownloaderFactory
from http_modules import Header, Request


class FormsIndexReader(IndexFileReader, ABC):
    index_type = 'Forms'


class DefaultFormsIndexReader(IndexFileReader):
    def read(self, index_data: str) -> list:
        data = []
        pattern = re.compile('13F-HR[^/A]{2}.*\n')
        lines = re.findall(pattern, index_data)

        for line in lines:
            line = line[:-1]
            columns = self._split_line(line)
            data.append(
                FormIndexData(
                    form_type=columns['form'],
                    company_name=columns['name'],
                    date_filed=columns['date'],
                    cik=int(columns['cik']),
                    file_name=columns['file']
                )
            )

        return data

    def _split_line(self, line: str):
        columns = {
            'form': line[0:12].strip(),
            'name': line[12:74].strip(),
            'cik': line[74:86].strip(),
            'date': line[86:98].strip(),
            'file': line[98:].strip()
        }

        return columns


class FormsIndexReaderFactory:
    def __call__(self, reader_type: str = 'default'):
        match reader_type:
            case 'default' | 'Default':
                return DefaultFormsIndexReader()
            case _:
                raise Exception()


class FormsIndexWriter(IndexWriter, ABC):
    index_type = 'Forms'


class PostrgresFormIndexWriter(IndexWriter):
    def write(self, sources: list[FormIndexData]):
        manager = connection_manager()
        with manager:
            for source in sources:
                insert_query = sql.SQL(
                    """INSERT INTO source (id, company_name, date_filed, cik, file_name)
                            VALUES ({}, {}, {}, {}, {})"""
                ).format(
                    sql.Literal(uuid4().hex),
                    sql.Literal(source.company_name),
                    sql.Literal(source.date_filed),
                    sql.Literal(source.cik),
                    sql.Literal(source.file_name)
                )
                manager.cursor.execute(insert_query)


class FormsIndexWriterFactory:
    def __call__(self, writer_type: str = 'default'):
        match writer_type:
            case 'default' | 'Default' | 'postgres' | 'Postgres':
                return PostrgresFormIndexWriter()
            case _:
                raise Exception()


class FormsIndexFileManager(
    IndexFileManager,
    index_type='form',
    downloader_factory=DownloaderFactory(),
    reader_factory=FormsIndexReaderFactory(),
    writer_factory=FormsIndexWriterFactory(),
):
    def __init__(self, downloader: str = 'default', reader: str = "default", writer: str = "default"):
        super().__init__(downloader=downloader, reader=reader, writer=writer)
        self._errors = []

    def run(self, url: str):
        self._count += 1
        request = Request(header=Header(), url=url)
        print(f"***Downloading form index file from {url}.***")
        response = self.downloader.download(request, max_retries=2)
        if response.errors:
            self._errors.append(response.errors)
            print(f"==> Download Failed")
            return
        print('==> Download successful.')
        print("Reading index file.")
        sources = self.reader.read(response.data)
        print('==> Done reading.')
        print('Writing index data.')
        self.writer.write(sources)
        print('==> Print done writing.')
