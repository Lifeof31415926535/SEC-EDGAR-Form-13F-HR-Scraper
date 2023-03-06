import psycopg2
import psycopg2.sql as sql

from abc import ABC, abstractmethod

from abstracts import SourceReader
from data.index_data import FormIndexData
from db import connection_manager
from periods import FilingDate, QuarterFilingDate, BoundaryState, MonthFilingDate


class PostgresFormSourceReader(SourceReader):
    def __init__(self, batch_size: int, **kwargs):
        self.query = self._make_query(**kwargs)
        super().__init__(batch_size=batch_size)

    def _make_query(self, **kwargs) -> sql.Composable:
        print(kwargs)
        match kwargs:
            case {'year': y, **more} if not more:
                start = f"{y}-01-01"
                end = f"{y}-12-31"
                return sql.SQL(
                    "SELECT * FROM source WHERE filing_date BETWEEN {} AND {}"
                ).format(sql.Literal(start), sql.Literal(end))
            case {'year': y, 'quarter': q, **more} if not more:
                start = QuarterFilingDate(year=y, quarter=q, boundary=BoundaryState.START).date_str_formatted('-')
                end = QuarterFilingDate(year=y, quarter=q, boundary=BoundaryState.END).date_str_formatted('-')
                return sql.SQL(
                    "SELECT * FROM source WHERE filing_date BETWEEN {} AND {}"
                ).format(sql.Literal(start), sql.Literal(end))
            case {'year': y, 'month': m, **more} if not more:
                start = MonthFilingDate(year=y, month=m, boundary=BoundaryState.START).date_str_formatted('-')
                end = MonthFilingDate(year=y, month=m, boundary=BoundaryState.END).date_str_formatted('-')
                return sql.SQL(
                    "SELECT * FROM source WHERE filing_date BETWEEN {} AND {}"
                ).format(sql.Literal(start), sql.Literal(end))
            case {'start': st, 'end': en}:
                return sql.SQL(
                    "SELECT * FROM source WHERE filing_date BETWEEN {} AND {}"
                ).format(sql.Literal(st), sql.Literal(en))
            case {'date': dt}:
                return sql.SQL(
                    "SELECT * FROM source WHERE filing_date = {}"
                ).format(sql.Literal(dt))
            case _:
                raise Exception('')

    def _initialize(self):
        manager = connection_manager()

        with manager:
            manager.cursor.execute(self.query)
            self._sources = [FormIndexData(
                id=tp[0],
                form_type='13F-HR',
                company_name=tp[1],
                date_filed=tp[2].strftime('%Y%m%d'),
                cik=tp[3],
                file_name=tp[4]
            ) for tp in manager.cursor.fetchall()]


if __name__ == '__main__':
    sr = PostgresFormSourceReader(batch_size=20, year=2022)
    print(list(sr)[0][0])
