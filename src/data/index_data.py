from dataclasses import dataclass


@dataclass
class FormIndexData:
    form_type: str
    company_name: str
    date_filed: str
    cik: int
    file_name: str
