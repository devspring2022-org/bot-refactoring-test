from .request import Request
from .objects import CommonObject


class File(CommonObject):
    def __init__(self,
                 request: Request,
                 url: str,
                 data: dict,
                 restricted: bool = False):
        super().__init__(request, url, data, restricted)
        self.name = self._data["name"]
        self.path = self._data["path"]
        self.sha = self._data["sha"]
        self.size = self._data["size"]
        self.url = self._data["url"]
        self.html_url = self._data["html_url"]
        self.git_url = self._data["git_url"]
        self.download_url = self._data["download_url"]
        self.type = self._data["type"]
        self.content = self._data["content"]
        self.encoding = self._data["encoding"]
        self._links = self._data["_links"]

    def get_content(self):
        _, data = self._request.request_text("GET", self.download_url)
        return data
