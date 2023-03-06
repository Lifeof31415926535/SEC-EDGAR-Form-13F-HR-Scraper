from dataclasses import dataclass, field


@dataclass
class FormIndexData:
    form_type: str
    company_name: str
    date_filed: str
    cik: int
    file_name: str
    id: str = field(default=None)
