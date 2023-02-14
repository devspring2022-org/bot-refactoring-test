from time import time, sleep
from datetime import datetime, timedelta
import requests


class Request():
    def __init__(self,
                 host: str,
                 token: str or None = None,
                 user_agent: str = "MOEVM-GitHub-Bot",
                 limits_check_sleep_time: int = 5):
        self._authorization = f"token {token}"
        self.host = host
        self._user_agent = user_agent
        self._session = requests.Session()
        self._limits_check_sleep_time = limits_check_sleep_time
        self._headers = {
            "Authorization": self._authorization,
            "Content-Type": "application/json",
            "User-Agent": self._user_agent
        }
        self._data = ""
        self._params = {
            "page": 1,
            "per_page": 10
        }

    def set_headers(self, headers: dict = {}):
        self._headers = {
            "Authorization": self._authorization,
            "Content-Type": "application/json",
            "User-Agent": self._user_agent
        }
        for key, value in headers.items():
            self._headers[key] = value

    def set_data(self, data: dict = {}):
        self._data = str(data).replace('\'', '\"')

    def set_params(self, params: dict = {}):
        self._params = {
            "page": 1,
            "per_page": 100
        }
        for key, value in params.items():
            self._params[key] = value

    def _get_link(self, headers: dict[str, str], type: str) -> str or None:
        links = headers.get("Link")
        if links is not None:
            parsed_links = links.split(", ")
            for link in parsed_links:
                if link.endswith(f'; rel="{type}"'):
                    return link.split(";")[0][1:-1]
        return None

    def request(self, operation: str, api_url: str):
        operation = getattr(self._session, operation.lower())
        if api_url.startswith("/"):
            api_url = f"{self.host}{api_url}"
        response = operation(api_url,
                             headers=self._headers,
                             data=self._data,
                             params=self._params)
        #print(response.headers["X-RateLimit-Remaining"])
        return response

    def check_status_code(self, response):
        if response.status_code >= 400:
            raise Exception(response.text)

    def rate_limit_handler(self, response):
        headers = response.headers
        if response.status_code == 403 and int(headers["X-RateLimit-Remaining"]) == 0:
            data = response.json()
            if data.get("message", "").startswith("API rate limit exceeded for "):
                reset_timestamp = int(headers.get("X-RateLimit-Reset"))
                reset_date_gmt3 = datetime.fromtimestamp(reset_timestamp) + timedelta(hours=3)
                print(f"Достигнут лимит запросов. Работа бота продолжится {reset_date_gmt3}")
                while time() < reset_timestamp:
                    sleep(self._limits_check_sleep_time)
                return True
        return False

    def request_with_check(self, operation: str, url: str):
        response = self.request(operation, url)
        if self.rate_limit_handler(response):
            response = self.request(operation, url)
        self.check_status_code(response)
        headers = response.headers
        data = response.json()
        self.set_headers()
        self.set_data()
        self.set_params()
        return headers, data

    def request_list_with_check(self, operation: str, url: str):
        all_data = []
        self._params.pop("page")
        while url is not None:
            response = self.request(operation, url)
            if self.rate_limit_handler(response):
                response = self.request(operation, url)
            self.check_status_code(response)
            headers = response.headers
            url = self._get_link(headers, "next")
            data = response.json()
            if len(data) == 0:
                break
            all_data = all_data + data
        self.set_headers()
        self.set_data()
        self.set_params()
        return headers, all_data

    def request_text(self, operation: str, url: str):
        response = self.request(operation, url)
        self.check_status_code(response)
        headers = response.headers
        data = response.text
        self.set_headers()
        self.set_data()
        self.set_params()
        return headers, data