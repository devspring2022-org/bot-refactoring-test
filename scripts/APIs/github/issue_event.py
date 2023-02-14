from .request import Request
from .objects import CommonObject


class IssueEvent(CommonObject):
    def __init__(self,
                 request: Request,
                 url: str,
                 data: dict,
                 restricted: bool = False):
        super().__init__(request, url, data, restricted)
        self.id = self._data["id"]
        self.node_id = self._data["node_id"]
        self.url = self._data["url"]
        self.actor = self._data["actor"]
        self.event = self._data["event"]
        self.commit_id = self._data["commit_id"]
        self.commit_url = self._data["commit_url"]
        self.created_at = self._data["created_at"]


    def print(self):
        return self._data