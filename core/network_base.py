import requests
from core.config import config
from core.errors import NetworkError, APIError, CityNotFoundError

class BaseAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_request(self, endpoint: str, method="GET", params=None, headers=None, response_type="json"):
        """
        Generic request handler.
        :param endpoint: API endpoint path.
        :param method: HTTP method (GET, POST, etc).
        :param params: URL parameters.
        :param headers: HTTP headers.
        :param response_type: Expected return type ('json' or 'content').
        """
        url = self.base_url + endpoint.lstrip('/')
        
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                timeout=config.TIMEOUT
            )

            # Handle 404 specifically for weather requests
            if response.status_code == 404:
                city = params.get('q', 'Unknown') if params else 'Unknown'
                raise CityNotFoundError(city)

            # Raise exceptions for 4xx and 5xx status codes
            response.raise_for_status()

            if response_type == "json":
                return response.json()
            if response_type == "content":
                return response.content
            return response

        except requests.exceptions.ConnectionError:
            raise NetworkError()
        except requests.exceptions.HTTPError as e:
            raise APIError(f"Server returned an error: {e}")