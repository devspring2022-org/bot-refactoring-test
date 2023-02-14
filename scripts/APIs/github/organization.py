from .request import Request
from .objects import CommonObject
from .team import Team
from .repository import Repository


class Organization(CommonObject):
    def __init__(self,
                 request: Request,
                 url: str,
                 data: dict,
                 restricted: bool = False):
        super().__init__(request, url, data, restricted)
        self.login = self._data["login"]

    def print(self):
        print(self._data.keys())

    def get_members(self, restricted: bool = True):
        url = f"/orgs/{self.login}/members"
        _, data = self._request.request_with_check("GET", url)
        ### Переделать?
        return list(set([member["login"] for member in data]))

    def get_team(self, name: str):
        url = f"/orgs/{self.login}/teams/{name}"
        _, data = self._request.request_with_check("GET", url)
        return Team(self._request, url, data)

    def get_teams(self, restricted: bool = True):
        url = f"{self._url}/teams"
        _, data = self._request.request_list_with_check("GET", url)
        teams = []
        for team in data:
            teams.append(Team(self._request, f"{url}/{team['name']}", team, True) if restricted else self.get_team(team["name"]))
        return teams
    
    def get_repository(self, name):
        url = f"/repos/{self.login}/{name}"
        _, data = self._request.request_with_check("GET", url)
        return Repository(self._request, url, data)
