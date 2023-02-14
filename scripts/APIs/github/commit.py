from .request import Request
from .objects import CommonObject


class Commit(CommonObject):
    def __init__(self,
                 request: Request,
                 url: str,
                 data: dict,
                 restricted: bool = False):
        super().__init__(request, url, data, restricted)
        self.sha = self._data["sha"]
        self.node_id = self._data["node_id"]
        self.commit = self._data["commit"]
        self.url = self._data["url"]
        self.html_url = self._data["html_url"]
        self.comments_url = self._data["comments_url"]
        self.author = self._data["author"]
        self.committer = self._data["committer"]
        self.parents = self._data["parents"]

    def print(self):
        return self._data