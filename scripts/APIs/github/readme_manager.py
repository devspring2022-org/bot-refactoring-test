from markdown import markdown
import pandas as pd

from APIs.config import Config

from .repository import Repository


class ReadmeManager():
    def __init__(self, repository: Repository):
        self.repository = repository
        self.readme_file = repository.get_readme()
        readme_settings = Config()["repository"]["main table"]
        readme_content_raw = self.readme_file.get_content()
        readme_html = markdown(readme_content_raw, extensions=["markdown.extensions.extra"])

        self.readme_df = pd.read_html(readme_html)[0].astype(object).fillna("").set_index("github")\
                         .rename(columns={readme_settings["last_name_column_name"]: "surname",
                                          readme_settings["first_name_column_name"]: "name"})
        work_columns_from = int(readme_settings["work_columns_range_start"]) - 1
        self._work_ids = self.readme_df.columns[work_columns_from:]
        self.students = self.readme_df.to_dict("index")

    def has_column(self, column_name: str) -> bool:
        return column_name in self.readme_df
    
    def get_student_by_github(self, github: str) -> dict or None:
        return self.students.get(github)
    
    def has_work_id(self, work_id) -> bool:
        return work_id in self._work_ids
