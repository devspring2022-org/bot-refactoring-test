from .request import Request
from .objects import CommonObject
from .pull_request import PullRequest
from .file import File


class Repository(CommonObject):
    def __init__(self,
                 request: Request,
                 url: str,
                 data: dict,
                 restricted: bool = False):
        super().__init__(request, url, data, restricted)
        self.full_name = self._data["full_name"]

    def print(self):
        print(self._data.keys())

    def get_contents(self, path: str = "", ref: str or None = None):
        params = {}
        if ref is not None:
            params["ref"] = ref
        self._request.set_params(params)
        url = f"{self._url}/contents/{path}"
        _, data = self._request.request_list_with_check("GET", url)
        print(type(data))
        for file in data:
            print(file)

    def get_pull_request(self, number: int):
        url = f"{self._url}/pulls/{number}"
        _, data = self._request.request_with_check("GET", url)
        return PullRequest(self._request, url, data)

    def get_pull_requests(self, restricted: bool = True) -> list[PullRequest]:
        url = f"{self._url}/pulls"
        _, data = self._request.request_list_with_check("GET", url)
        pull_requests = []
        for pull_request in data:
            pull_requests.append(PullRequest(self._request, f"{url}/{pull_request['number']}", pull_request, True) if restricted else self.get_pull_request(pull_request["number"]))
        return pull_requests

    def get_readme(self) -> File:
        url = f"{self._url}/readme"
        _, data = self._request.request_with_check("GET", url)
        return File(self._request, url, data)