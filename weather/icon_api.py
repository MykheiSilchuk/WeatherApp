from core.network_base import BaseAPIClient
from core.config import config


class WeatherIconAPI(BaseAPIClient):

    def __init__(self):

        super().__init__(config.ICON_BASE_URL)

    def get_icon(self, icon_code: str):

        endpoint = f"{icon_code}@2x.png"

        return self.make_request(
            endpoint=endpoint,
            response_type="content"
        )