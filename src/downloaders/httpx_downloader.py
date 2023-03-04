import httpx

from abstracts import Downloader
from http_modules import Request, Response
from http_modules.requests import Header


class HttpxDownloader(Downloader):
    def download(self, request: Request, max_retries) -> Response:
        r = None
        retries = 0
        errors = None

        with httpx.Client(
                headers={'user-agent': request.header.user_agent},
                timeout=request.header.timeout
        ) as client:
            while retries < max_retries:
                errors = []
                try:
                    r = client.get(url=request.url)
                except httpx.HTTPError as http_err:
                    errors.append({'HTTP Error': http_err})
                    continue

                if r.status_code < 300:
                    return Response(
                        url=request.url,
                        status=200,
                        retries=retries,
                        errors=[],
                        data=r.text
                    )
                retries += 1

        errors.append({f"Status {r.status_code}": f"Failed to download {request.url}."})

        return Response(
            url=request.url,
            status=r.status_code,
            retries=retries,
            errors=errors,
            data=None
        )


if __name__ == '__main__':
    d = HttpxDownloader()
    h = Header()
    req = Request(
        url='https://www.sec.gov/Archives/edgar/daily-index/2022/QTR1/form.20220107.idx',
        header=h
    )
    print((d.download(request=req, max_retries=2).data).splitlines()[11:][0][74:86])
