from dataclasses import dataclass, field

from config import DEFAULT_USER_AGENT, DEFAULT_TIMEOUT


@dataclass
class Header:
    user_agent: str = DEFAULT_USER_AGENT
    timeout: int = DEFAULT_TIMEOUT


@dataclass
class Request:
    header: Header
    url: str
