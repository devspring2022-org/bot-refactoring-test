from typing import NamedTuple

from APIs.config import Config

from .repository import Repository


class RepositoryManager():
    def __init__(self, repository: Repository):
        self._repository = repository

    def build_dir_structure(self, init_dir: str = "", branch_name: str = "master"):
        class Directory(NamedTuple):
            files: list
            subdirs: dict

        def walk(curr_dir):
            structure = Directory(files=[], subdirs={})
            for content_piece in self._repository.get_contents(curr_dir, ref=branch_name):
                if content_piece.type == 'dir':
                    structure.subdirs[content_piece.name] = walk(f'{curr_dir}/{content_piece.name}')
                else:
                    structure.files.append(content_piece.name)
            return structure
        return walk(init_dir)
