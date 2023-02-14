from .request import Request
from .repository import Repository
from .organization import Organization


class GitHub():
    def __init__(self, token: str):
        self._request = Request(host="https://api.github.com",
                                token=token)

    def get_repository(self, full_name: str):
        url = f"/repos/{full_name}"
        _, data = self._request.request_with_check("GET", url)
        return Repository(self._request, url, data)

    def get_organization(self, organization_name: str):
        url = f"/orgs/{organization_name}"
        _, data = self._request.request_with_check("GET", url)
        return Organization(self._request, url, data)
