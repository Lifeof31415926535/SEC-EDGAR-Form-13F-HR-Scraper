from dataclasses import dataclass

from src.periods import FilingDate


@dataclass
class FilingSource:
    date: FilingDate
    url_path: str
    file_type: str

