import re

from abstracts import IndexFileReader
from src.data.index_data import FormIndexData


class FormIndexReader(IndexFileReader):
    def read(self, index_data: str) -> list:
        data = []
        pattern = re.compile('13F-HR[^/A]{2}.*\n')
        lines = re.findall(pattern, index_data)

        for line in lines:
            line = line[:-1]
            columns = self._split_line(line)
            print(line)
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
