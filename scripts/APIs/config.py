"""
Модуль работы с конфигурационными файлами
"""

import json
import re

from APIs.singleton import Singleton


class Config(metaclass=Singleton):
    """
    Данный класс представляет собой контейнер для хранения конфигураций бота
    """
    def __init__(self,
                 repository_full_name: str or None = None,
                 config_path: str = "/config",
                 **files):
        self._config = {}
        
        for config_name, filename in files.items():
            try:
                with open(config_path + filename, mode="r", encoding="utf-8") as file:
                    self._config[config_name] = json.load(file)
            except FileNotFoundError as error:
                error.strerror = "Конфигурационный файл не найден"
                raise error

        if repository_full_name is not None:
            self.set_repository_config(repository_full_name)

    def __getitem__(self, key):
        if key not in self._config:
            raise KeyError(f"В конфигурационном файле отсутствует секция '{key}'.")
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value
    
    def __contains__(self, item):
        return item in self._config

    def set_repository_config(self, repository_full_name: str) -> None:
        if "repositories" not in self._config:
            raise KeyError("В конфигурационном файле отсутствует секция 'repositories'.")
        for reg_repository_name in self._config["repositories"]:
            if re.fullmatch(reg_repository_name, repository_full_name):
                self._config["repository"] = self._config["repositories"][reg_repository_name]
                return
        raise KeyError(f"В конфигурационном файле не найден репозиторий {repository_full_name}.")

    def get_repository_config(self, repository_full_name: str or None = None) -> dict:
        if repository_full_name is None:
            if "repository" not in self._config:
                raise KeyError("В конфигурационном файле отсутствует секция 'repository'.")
            return self._config["repository"]
        if "repositories" not in self._config:
            raise KeyError("В конфигурационном файле отсутствует секция 'repositories'.")
        for reg_repository_name in self._config["repositories"]:
            if re.fullmatch(reg_repository_name, repository_full_name):
                return self._config["repositories"][reg_repository_name]
        return None
