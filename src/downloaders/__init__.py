from abstracts import Downloader
from httpx_downloader import HttpxDownloader


class DownloaderFactory:
    def __call__(self, downloader_type: str) -> Downloader:
        match downloader_type:
            case 'default' | 'Default' | 'httpx' | 'HTTPX':
                return HttpxDownloader()
            case _:
                raise Exception()
