"""
Автоматическая проверка pull request студента на соответствие требованиям форматирования и
других необходимых параметров

Вызов скрипта: python3 check_pull_request github_token number_of_pr repository_name author

Аргументы:
    github_token:
        GitHub токен
    number_of_pr:
        номер pull request, участвующего в выполнении команды
    repository_name:
        полное название репозитория в формате <user or org>/<repository>
    author:
        логин автора события
"""

from APIs.monad import Monad
from APIs.log import common_log
from APIs.config import Config
from APIs.github import (GitHub,
                         ReadmeManager,
                         CommentManager,
                         PullRequestManager,
                         RightAccessManager)


@common_log
class CheckPullRequest():
    def __init__(self, arguments_dict):
        self._github_token = arguments_dict["github_token"]
        self._number_of_pr = arguments_dict["number_of_pr"]
        self._repository_name = arguments_dict["repository_name"]
        self._author = arguments_dict["author"]

        self._github = GitHub(Config()["auth"]["pat_token"])
        self._repository = self._github.get_repository(self._repository_name)
        self._repository.get_contents("README.md")
        self._pull_request = self._repository.get_pull_request(self._number_of_pr)

        self._authorized_accounts = ["mahalichev"] #RightAccessManager().get_authorized_accounts()
        self._readme_manager = ReadmeManager(self._repository)
        self._pull_request_manager = PullRequestManager(self._pull_request)

    def run(self):
        self.log.info("Начата проверка pull request")
        """
        monad = Monad("passed").next(self.check_for_duplicate)\
                               .next(self.check_pull_request_style)\
                               .next(self.check_moodle_course)
        print(monad.get_result())
        """

    def check_for_duplicate(self):
        self.log.info("Начат поиск дубликатов pull request")

    def check_pull_request_style(self) -> str:
        self.log.info("Начата стилистическая проверка pull request")
        monad = Monad(True).next(self._pull_request_manager.check_labels,
                                 authorized_accounts=self._authorized_accounts)\
                           .next(self._pull_request_manager.check_title,
                                 readme_manager=self._readme_manager)\
                           .next(self._pull_request_manager.check_branch)\
                           .next(self._pull_request_manager.check_commits)
        return "passed" if monad.get_result() else "failed"

    def check_moodle_course(self):
        self.log.info("Начата проверка соответствующего курса на Moodle")


