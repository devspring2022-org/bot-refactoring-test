
from APIs.config import Config
from APIs.utilities import match_list

from .github import GitHub
from .url_parser import URLParser


class RightAccessManager():
    """
    Данный класс предназначен для формирования списков авторизованных пользователей (преподавателей).
    """
    def __init__(self, token: str):
        self._github = GitHub(token)

    def get_authorized_accounts(self,
                                settings: dict = {},
                                repository_config: dict = {}) -> list:
        accounts = ["github-actions\\[bot\\]"]

        if "authorized_accounts" in repository_config:
            accounts += repository_config["authorized_accounts"]

        if "organization_url" in settings:
            if "authorized_teams" in repository_config:
                accounts += self.get_teachers_from_teams(repository_config["authorized_teams"],
                                                         settings["organization_url"])
            else:
                accounts += self.get_teachers_from_organization(settings["organization_url"])
        return accounts

    def get_teachers_from_organization(self, organization_url: str) -> list:
        teachers = []
        organization_name = URLParser.parse_organization_name(organization_url)
        for member in self._github.get_organization(organization_name).get_members():
            teachers.append(member.login)
        return teachers
    
    def get_teachers_from_teams(self, re_teams: list, organization_url: str) -> list:
        teachers = []
        organization_name = URLParser.parse_organization_name(organization_url)
        organization_teams = self._github.get_organization(organization_name).get_teams()
        for team in organization_teams:
            if match_list(team["name"], re_teams):
                for member in team.get_members():
                    if member.login not in teachers:
                        teachers.append(member.login)
        return teachers

    def is_teacher(self, username: str, organization_url: str) -> bool:
        return username in self.get_teachers_from_organization(organization_url)
