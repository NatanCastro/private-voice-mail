import requests
from result import Err, Ok, Result
from core.ports.request_service import T, IRequestService, ResponseKind


class RequestService(IRequestService):
    def get(self, url: str, response_kind: ResponseKind) -> Result[T, str]:
        response = requests.get(url)
        
        match response_kind:
            case ResponseKind.JSON:
                try:
                    json_data = response.json()  # Expect dict
                    return Ok(json_data)  # Return Ok with dict type
                except Exception as e:
                    return Err(f"Could not transform response to JSON: {e}")
            case ResponseKind.RAW:
                return Ok(bytes(response.content))  # Return Ok with bytes type
            case _:
                raise ValueError("Unsupported ResponseKind")
