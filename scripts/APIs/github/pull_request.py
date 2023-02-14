from .request import Request
from .objects import CommonObject
from .commit import Commit
import APIs.github.repository
from .issue_event import IssueEvent


class PullRequest(CommonObject):
    def __init__(self,
                 request: Request,
                 url: str,
                 data: dict,
                 restricted: bool = False):
        super().__init__(request, url, data, restricted)
        self.url = self._data["url"]
        self.id = self._data["id"]
        self.node_id = self._data["node_id"]
        self.html_url = self._data["html_url"]
        self.diff_url = self._data["diff_url"]
        self.patch_url = self._data["patch_url"]
        self.issue_url = self._data["issue_url"]
        self.number = self._data["number"]
        self.state = self._data["state"]
        self.locked = self._data["locked"]
        self.title = self._data["title"]
        self.user = self._data["user"]
        self.body = self._data["body"]
        self.created_at = self._data["created_at"]
        self.updated_at = self._data["updated_at"]
        self.closed_at = self._data["closed_at"]
        self.merged_at = self._data["merged_at"]
        self.merge_commit_sha = self._data["merge_commit_sha"]
        self.assignee = self._data["assignee"]
        self.assignees = self._data["assignees"]
        self.requested_reviewers = self._data["requested_reviewers"]
        self.requested_teams = self._data["requested_teams"]
        self.labels = self._data["labels"]
        self.milestone = self._data["milestone"]
        self.draft = self._data["draft"]
        self.commits_url = self._data["commits_url"]
        self.review_comments_url = self._data["review_comments_url"]
        self.review_comment_url = self._data["review_comment_url"]
        self.comments_url = self._data["comments_url"]
        self.statuses_url = self._data["statuses_url"]
        self.head = self._data["head"]
        self.base = self._data["base"]
        self._links = self._data["_links"]
        self.author_association = self._data["author_association"]
        self.auto_merge = self._data["auto_merge"]
        self.active_lock_reason = self._data["active_lock_reason"]
        #Custom attributes
        self.repo_url = self._url.replace(f"/pulls/{self.number}", "")
        self.head_repo = APIs.github.repository\
                        .Repository(self._request, f"/repos/{self.head['repo']['full_name']}",
                                    self.head['repo'], True)

    def get_event(self, id):
        url = f"{self.issue_url.replace(f'/{self.number}', '')}/events/{id}"
        _, data = self._request.request_with_check("GET", url)
        return IssueEvent(self._request, url, data)

    def get_events(self, restricted: bool = True) -> list[IssueEvent]:
        url = f"{self.issue_url}/events"
        _, data = self._request.request_list_with_check("GET", url)
        events = []
        for event in data:
            event_url = f"{self.issue_url.replace(f'/{self.number}', '')}/events/{event['id']}"
            events.append(IssueEvent(self._request, event_url, event, True)
                                     if restricted else self.get_commit(event["id"]))
        return events

    def get_commit(self, sha: str) -> Commit:
        url = f"{self.repo_url}/commits/{sha}"
        _, data = self._request.request_with_check("GET", url)
        return Commit(self._request, url, data)

    def get_commits(self, restricted: bool = True) -> list[Commit]:
        url = f"{self._url}/commits"
        _, data = self._request.request_list_with_check("GET", url)
        commits = []
        for commit in data:
            commits.append(Commit(self._request, f"{self.repo_url}/commits/{commit['sha']}",        
                                  commit, True)
                           if restricted else self.get_commit(commit["sha"]))
        return commits

    def comment(self, comment):
        print(comment)

    def update(self,
               title: str or None = None,
               data: str or None = None,
               state: str or None = None,
               base: str or None = None,
               maintainer_can_modify: bool or None = None):
        request_data = {}
        if title is not None:
            request_data["title"] = title
        if data is not None:
            request_data["data"] = data
        if state is not None:
            request_data["state"] = state
        if base is not None:
            request_data["base"] = base
        if maintainer_can_modify is not None:
            request_data["maintainer_can_modify"] = maintainer_can_modify
        self._request.set_data(request_data)

        _, self._data = self._request.request_with_check("PATCH", self._url)
        self._fill_attributes()
        self._restricted = False
