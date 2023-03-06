import psycopg2.sql as sql

from uuid import uuid4

from abstracts import TableWriter
from data.filing_data import FilingData, PrimaryTableData, InfoTableData
from db import connection_manager


class PostgresTableWriter(TableWriter):
    def _write_filing(self, header: PrimaryTableData, filing_id, source_id):
        manager = connection_manager()
        write_query = sql.SQL(
            """INSERT INTO filing (filing_id, source_id, cik, company_name, period_of_report)
                VALUES ({}, {}, {}, {}, {});"""
        ).format(
            sql.Literal(filing_id),
            sql.Literal(source_id),
            sql.Literal(header.cik),
            sql.Literal(header.company_name),
            sql.Literal(header.period_of_report)
        )

        with manager:
            manager.cursor.execute(
                write_query
            )

    def _holding_to_sql(self, holding: InfoTableData, filing_id: str):
        return sql.SQL(
            "({}, {}, {}, {}, {}, {}, {}, {}, {}, {})"
        ).format(
            sql.Literal(filing_id),
            sql.Literal(holding.name_of_issuer),
            sql.Literal(holding.cusip),
            sql.Literal(holding.value),
            sql.Literal(holding.shrs_or_prn_amt.ssh_prnamt),
            sql.Literal(holding.shrs_or_prn_amt.ssh_prnamt_type),
            sql.Literal(holding.voting_authority.sole),
            sql.Literal(holding.voting_authority.shared),
            sql.Literal(holding.voting_authority.none),
            sql.Literal(holding.put_call)
        )

    def _write_filing_info(self, holdings: list[InfoTableData], filing_id):
        manager = connection_manager()
        insert_values = [self._holding_to_sql(holding, filing_id) for holding in holdings]
        insert_query = sql.Composed([
            sql.SQL("""INSERT INTO filing_info (
                filing_id,
                name_of_issuer, 
                cusip,
                value,
                ssh_prnamt, ssh_prnamt_type, 
                va_sole, 
                va_shared,
                va_none,
                put_call
                )
                VALUES"""),
            sql.SQL(",\n").join(insert_values),
            sql.SQL(";")
        ])

        with manager:
            manager.cursor.execute(
                insert_query
            )

    def write(self, data: FilingData, source_id: str):
        self._write_filing(data.header, data.filing_id, source_id)
        self._write_filing_info(data.info, data.filing_id)


class TableWriterFactory:
    def __call__(self, writer_type) -> TableWriter:
        match writer_type:
            case 'default' | 'Default' | 'postgres' | 'Postgres':
                return PostgresTableWriter()
            case _:
                raise Exception('')
