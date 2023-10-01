import ujson

from theHarvester.discovery.constants import MissingKey
from theHarvester.lib.core import AsyncFetcher, Core


class SearchCertsio:
    def __init__(self, word) -> None:
        self.word = word
        self.key = Core.certsio_key()
        if self.key[0] is None:
            raise MissingKey("Certsio")
        self.totalhosts: list = []
        self.proxy = False

    async def do_search(self) -> None:
        url = "https://certs-io1.p.rapidapi.com/certificates"
        payload = {
            "field": "domain",
            "page": 0,
            "term": f"{self.word}"
        }

        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": f"{self.key}",
            "X-RapidAPI-Host": "certs-io1.p.rapidapi.com",
        }
        response = await AsyncFetcher.post_fetch(url, data=ujson.dumps(payload), json=True, headers=headers, proxy=self.proxy)
        self.totalhosts = response
        print(response)

    async def get_hostnames(self) -> list:
        return self.totalhosts

    async def process(self, proxy: bool = False) -> None:
        self.proxy = proxy
        await self.do_search()
