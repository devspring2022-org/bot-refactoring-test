import re


class URLParser:
    """
    Данный класс предоставляет методы для парсинга различной информации из URL GitHub
    """
    @staticmethod
    def parse_repository_full_name(url: str) -> str:
        matches = re.match("^https?://github.com/([\\w-]+)/([\\w-]+)(/.*)*", url)
        if matches is None:
            raise ValueError(f"Невозможно получить полное имя репозитория. Некорректный формат URL: '{url}'")
        return matches[1] + '/' + matches[2]

    @staticmethod
    def parse_pull_request_number(url: str) -> int:
        matches = re.match("^https?://github.com/([\\w-]+)/([\\w-]+)/pull/(\\d+)(/.*)*", url)
        if matches is None:
            raise ValueError(f"Невозможно получить номер PR. Некорректный формат URL: '{url}'")
        return int(matches[3])

    @staticmethod
    def parse_organization_name(url: str) -> str:
        matches = re.match("^https?://github.com/([\\w-]+)(/.*)*", url)
        if matches is None:
            raise ValueError("Невозможно получить список преподавателей из организации. "
                            f"Некорректный формат URL: '{url}'")
        return matches[1]

    @staticmethod
    def parse_api_url_to_url(url: str, host: str) -> str:
        return url.replace(host, "")