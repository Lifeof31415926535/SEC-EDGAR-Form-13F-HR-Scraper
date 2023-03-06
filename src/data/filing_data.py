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
    cik: str = field(default=None)
    company_name: str = field(default=None)
    period_of_report: str = field(default=None)
    table_entry_total: int = field(default=None)
    table_value_total: int = field(default=None)
    errors: list[dict] = field(default_factory=list, init=False)


@dataclass
class InfoTableData:
    name_of_issuer: str = field(default=None)
    title_of_class: str = field(default=None)
    cusip: str = field(default=None)
    value: int = field(default=None)
    shrs_or_prn_amt: ShrsOrPrnAmt = field(default=None)
    investment_discretion: str = field(default=None)
    voting_authority: VotingAuthority = field(default=None)
    put_call: str = field(default=None)
    errors: list[dict] = field(default_factory=list, init=False)


@dataclass
class FilingData:
    filing_id: str = field(default=None)
    header: PrimaryTableData = field(default=None)
    info: list[InfoTableData] = field(default=None)
    filing_total: int = field(default=None)
    filing_errors: list[dict] = field(default_factory=list)
