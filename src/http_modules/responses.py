from dataclasses import dataclass
from typing import Any


@dataclass
class Response:
    url: str
    status: int
    retries: int
    errors: list[dict]
    data: Any
