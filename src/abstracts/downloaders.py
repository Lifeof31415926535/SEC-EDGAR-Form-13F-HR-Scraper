from abc import ABC, abstractmethod

from http_modules import Request, Response
from utils.mixins import SingletonMixin

from http_modules.requests import Request


class Downloader(ABC):
    @abstractmethod
    def download(self, request: Request, max_retries) -> Response:
        pass





