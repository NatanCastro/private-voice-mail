from typing import Optional
from requests import get
from core.ports.request_service import RequestService

class RequestsService(RequestService):
    def get(self, url: str, params: Optional[dict] = None):
        response = get(url, params)
        response.raise_for_status()
        data = response.json()
        __import__('pprint').pprint(data)

        return data
