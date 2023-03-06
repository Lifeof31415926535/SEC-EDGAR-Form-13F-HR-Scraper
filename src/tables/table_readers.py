import re

from uuid import uuid4

from abstracts import TableReader
from data.filing_data import PrimaryTableData, InfoTableData, ShrsOrPrnAmt, VotingAuthority, FilingData
from xml import parse_xml, XMLParserError


class TxtTableReader(TableReader):
    def _extract_tables(self, data) -> (str, str):
        primary_tab_pattern = re.compile("<edgarSubmission.*>[\s\S]+<\/edgarSubmission>")
        info_tab_pattern = re.compile("<.*:{0,1}informationTable.*>[\s\S]+<\/.*informationTable>")
        primary_tab_xml = re.search(primary_tab_pattern, data).group(0)
        info_tab_xml = re.search(info_tab_pattern, data).group(0)
        #print(primary_tab_xml)
        #print(info_tab_xml)
        return primary_tab_xml, info_tab_xml

    def _read_primary_table(self, table_xml: str) -> PrimaryTableData:
        try:
            primary_doc = parse_xml(table_xml)
            print(primary_doc)
        except XMLParserError as xml_err:
            data = PrimaryTableData()
            data.errors.append({"XML Parser Error": str(xml_err)})
            return data

        try:
            primary_doc = primary_doc['edgarSubmission']
            cik = primary_doc['headerData']['filerInfo']['filer']['credentials']['cik']
            companyName = primary_doc['formData']['coverPage']['filingManager']['name']
            periodOfReport = primary_doc['headerData']['filerInfo']['periodOfReport']
            tableEntryTotal = int(primary_doc['formData']['summaryPage']['tableEntryTotal'])
            tableValueTotal = 1000 * int(primary_doc['formData']['summaryPage']['tableValueTotal'])
            return PrimaryTableData(
                cik=cik,
                company_name=companyName,
                period_of_report=periodOfReport,
                table_entry_total=tableEntryTotal,
                table_value_total=tableValueTotal
            )
        except KeyError:
            data = PrimaryTableData()
            data.errors.append({"Invalid Table Error": "The primary table could not be read."})
            return data

    def _read_info_table(self, table_xml: str) -> (list[InfoTableData], int):
        try:
            info_table = parse_xml(table_xml)
        except XMLParserError as xml_err:
            data = InfoTableData()
            data.errors.append({"XML Parser Error": str(xml_err)})
            return [data], 0

        try:
            table_holdings = info_table['informationTable']['infoTable']
        except KeyError:
            data = InfoTableData()
            data.errors.append({"Invalid Table Error": f"Unable to read info table data."})
            return [data], 0

        holdings = []
        filing_total = 0

        for table in table_holdings:
            try:
                nameOfIssuer = table["nameOfIssuer"]
                titleOfClass = table["titleOfClass"]
                cusip = table["cusip"]
                value = 1000 * int(table["value"])
                sshPrnamt = int(table["shrsOrPrnAmt"]["sshPrnamt"])
                sshPrnamtType = table["shrsOrPrnAmt"]["sshPrnamtType"]
                putCall = table["putCall"] if ("putCall") in table else None
                investmentDiscretion = table["investmentDiscretion"]
                sole = int(table["votingAuthority"]["Sole"])
                shared = int(table["votingAuthority"]["Shared"])
                none = int(table["votingAuthority"]["None"])

                shrs_or_prn_amt = ShrsOrPrnAmt(ssh_prnamt=sshPrnamt, ssh_prnamt_type=sshPrnamtType)
                voting_authority = VotingAuthority(sole=sole, shared=shared, none=none)

                holdings.append(
                    InfoTableData(
                        name_of_issuer=nameOfIssuer,
                        title_of_class=titleOfClass,
                        cusip=cusip,
                        value=value,
                        shrs_or_prn_amt=shrs_or_prn_amt,
                        put_call=putCall,
                        investment_discretion=investmentDiscretion,
                        voting_authority=voting_authority
                    )
                )
                filing_total += value
            except KeyError:
                data = InfoTableData()
                data.errors.append({"Invalid Holding Error": f"Unable to read holding data."})
                holdings.append(data)
        return holdings, filing_total

    def read(self, data: str) -> FilingData:
        primary_tab_xml, info_tab_xml = self._extract_tables(data)
        if not primary_tab_xml or not info_tab_xml:
            return FilingData(filing_errors=[{"Extraction Error": "No tables could be extracted form the data."}])
        primary_tab_data = self._read_primary_table(primary_tab_xml)
        info_tab_data, filing_total = self._read_info_table(info_tab_xml)
        return FilingData(
            filing_id=uuid4().hex,
            header=primary_tab_data,
            info=info_tab_data,
            filing_total=filing_total
        )


class TableReaderFactory:
    def __call__(self, reader_type: str) -> TableReader:
        match reader_type:
            case 'default' | 'Default' | 'postgres' | 'Postgres':
                return TxtTableReader()
            case _:
                raise Exception("")
