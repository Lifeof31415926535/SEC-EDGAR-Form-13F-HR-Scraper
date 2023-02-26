from dataclasses import dataclass, field


@dataclass
class ShrsOrPrnAmt:
    ssh_prnamt: int
    ssh_prnamt_type: str


@dataclass
class VotingAuthority:
    sole: int
    shared: int
    none: int


@dataclass
class PrimaryTableData:
    filing_id: str
    cik: str
    company_name: str
    period_of_report: str
    table_entry_total: int


@dataclass
class InfoTableData:
    name_of_issuer: str
    title_of_class: str
    cusip: str
    value: int
    shrs_or_prn_amt: ShrsOrPrnAmt
    investment_discretion: str
    voting_authority: VotingAuthority
    put_call: str = field(default=None)


@dataclass
class FilingData:
    header: PrimaryTableData
    info: list[InfoTableData]
    filing_total: int
