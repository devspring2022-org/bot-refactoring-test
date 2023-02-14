import re
from re import Match

from APIs.config import Config
from APIs.utilities import match_list

from .commit import Commit
from .issue_event import IssueEvent
from .pull_request import PullRequest
from .readme_manager import ReadmeManager
from .comment_manager import CommentManager
from .repository_manager import RepositoryManager

PULL_REQUEST_TITLE_REGEX = r"([A-Za-z\-\.]+)_([A-Za-z\_\.]+)_([A-Za-z\-\.]+)(\d+)"


class PullRequestManager():
    def __init__(self, pull_request: PullRequest):
        self._pull_request = pull_request
        self._events = None
        self._commits = None

    def _get_commits(self) -> list[Commit]:
        if self._commits is None:
            self._commits = self._pull_request.get_commits()
    
    def _get_events(self) -> list[IssueEvent]:
        if self._events is None:
            self._events = self._pull_request.get_events()

    def parse_title(self, regex: str) -> Match[str] or None:
        return re.fullmatch(regex, self._pull_request.title)

    def check_title(self, readme_manager: ReadmeManager) -> bool:
        wiki_url = Config()["repository"]["wiki_url"]

        matches = self.parse_title(PULL_REQUEST_TITLE_REGEX)
        if matches is None:
            CommentManager.comment_pull_request(self._pull_request,
                                                "wrong title format",
                                                wiki_url=wiki_url)
            return False

        surname, name, work_label, work_number = matches.groups()
        work_label = work_label.lower()
        work_id = f"{work_label}{work_number}"

        github_login = self._pull_request.user["login"]
        user_info = readme_manager.get_student_by_github(github_login)

        if user_info is None:
            print("Ошибочка")
            return False

        if (user_info["surname"] != surname) or (user_info["name"] != name):
            print("Ошибочка")
            return False
        
        if not match_list(work_label, Config()["repository"]["work_labels"]):
            print("Ошибочка")
            return False

        if not readme_manager.has_work_id(work_id):
            print("Ошибочка")
            return False
        return True

    def check_labels(self, authorized_accounts: list[str]) -> bool:
        self._get_events()
        unauthorized_labels = {}
        for event in self._events:
            if event.event not in ["labeled", "unlabeled"]:
                continue
            if event.actor["login"] not in authorized_accounts:
                label = event.label["name"]
                if unauthorized_labels.get(label) is None:
                    unauthorized_labels[label] = False
                unauthorized_labels[label] = not unauthorized_labels[label]

        if any(item for item in unauthorized_labels.values()):
            labels = [f"\'{key}\'" for key, value in unauthorized_labels.items() if value]
            CommentManager.comment_pull_request(self._pull_request,
                                                "unauthorized label",
                                                labels=", ".join(labels))
            return False
        return True

    def check_branch(self) -> bool:
        branch_name = self._pull_request.head["ref"]
        if branch_name.lower() != self._pull_request.title.lower():
            print("Ошибочка")
            return False
        
        head_repository = self._pull_request.head_repo
        #repository_manager = RepositoryManager(head_repository)
        #print(repository_manager.build_dir_structure("", branch_name))

        return True

    def check_commits(self) -> bool:
        self._get_commits()
        return True