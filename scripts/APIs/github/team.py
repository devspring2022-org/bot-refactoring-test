from .request import Request
from .objects import CommonObject


class Team(CommonObject):
    def __init__(self,
                 request: Request,
                 url: str,
                 data: dict,
                 restricted: bool = False):
        super().__init__(request, url, data, restricted)

    def data_keys(self):
        return self._data.keys()