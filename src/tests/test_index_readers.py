from unittest import TestCase
from tests.data.index_reader_data import INDEX_DATA

from src.index_sources.index_readers import FormIndexReader
from src.data.index_data import FormIndexData


class TestIndexFormIndexReader(TestCase):
    def setUp(self) -> None:
        self.valid_result = [
            FormIndexData(
                form_type='13F-HR',
                company_name='TLWM',
                cik=1732537,
                date_filed='20220204',
                file_name='edgar/data/1732537/0001085146-22-000524.txt'
            ),
            FormIndexData(
                form_type='13F-HR',
                company_name='TORONTO DOMINION BANK',
                cik=947263,
                date_filed='20220204',
                file_name='edgar/data/947263/0001654954-22-001088.txt'
            ),
            FormIndexData(
                form_type='13F-HR',
                company_name='TORRAY LLC',
                cik=98758,
                date_filed='20220204',
                file_name='edgar/data/98758/0000950123-22-001002.txt'
            ),
        ]

    def test_read(self):
        reader = FormIndexReader()
        self.assertEqual(self.valid_result, reader.read(INDEX_DATA))
