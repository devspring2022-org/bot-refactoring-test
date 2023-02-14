"""
Скрипт, реализующий паттерн проектирования "Фасад", предназначен для вызова необходимых задач,
выполняемых ботом

Для выполнения задачи в качестве аргумента передается команда и необходимые флаги

Для более подробной информации при запуске скрипта используйте флаг --help
"""


import sys
import logging
from argparse import ArgumentParser

from APIs.log import common_log, get_logs
from APIs.config import Config
from check_pull_request import CheckPullRequest


AVAILABLE_COMMANDS = {
    "check_pr": {
        "object": CheckPullRequest,
        "description": "Автоматизированная проверка pull request",
        "arguments": ["github_token", "number_of_pr", "repository_name", "author"]
    },
    "update_readme_grades": {
        "object": CheckPullRequest,
        "description": ("Актуализация оценок в файле README.MD на основе оценок, "
                        "поставленных в pull request-ы"),
        "arguments": ["ab", "bc", "cd", "de"]
    }
}

ARGUMENT_DESCRIPTIONS = {
    "github_token": "GitHub токен",
    "number_of_pr": "Номер pull request, участвующего в выполнении команды",
    "repository_name": "Полное название репозитория в формате <user or org>/<repository>",
    "author": "Логин автора события",
    "ab": "aaa",
    "bc": "bbb",
    "cd": "ccc",
    "de": "ddd"
}

PARSER_DESCRIPTION = ("Многофункциональный GitHub бот для поддержки процесса проверки "
                      "и защиты лабораторных и курсовых работ студентов")

ERROR_MISSING_COMMAND = ("Не была указана команда для выполнения. "
                         "Используйте {filename} --help для подробной информации")

ERROR_MISSING_ARGS = ("Недостаточно аргументов для выполнения данной команды. "
                      "Используйте {filename} {command} --help для подробной информации")


@common_log
class Facade():
    def parse_arguments(self):
        """
        Генерация парсера и последующий парсинг аргументов, переданных скрипту через командную строку
        """
        parser = ArgumentParser(description=PARSER_DESCRIPTION,
                                epilog = ("Для более подробной информации используйте: "
                                        f"{sys.argv[0]} <command> --help"))
        subparsers = parser.add_subparsers(help="sub-command help")

        for command, command_data in AVAILABLE_COMMANDS.items():
            subparser = subparsers.add_parser(command, help=command_data["description"])
            subparser.set_defaults(command=command)
            for argument in command_data["arguments"]:
                subparser.add_argument("-" + argument, help=ARGUMENT_DESCRIPTIONS[argument])
        return parser.parse_args()

    def run_process(self, command, arguments_dict):
        Config(repository_full_name=arguments_dict.get("repository_name"),
               config_path="../config",
               auth="/auth.json",
               settings="/settings.json",
               repositories="/repositories.json",
               tables="/auth.json")
        self.log.info("asda")
        object_to_exec = AVAILABLE_COMMANDS[command]["object"]
        object_to_exec(arguments_dict).run()
        self.log.critical("asd123123")
        #10/0

    def __init__(self):
        """
        Запуск основной логики скрипта
        """
        self.log.info("Начата работа бота")
        self._logger = logging.getLogger(self.__class__.__name__)
        input_arguments = self.parse_arguments()
        input_arguments_dict = vars(input_arguments)

        command = input_arguments_dict.pop("command", None)
        if command is None:
            self.log.critical("В переданных аргументах не найдена команда для выполнения")
            raise KeyError(ERROR_MISSING_COMMAND.format(filename=sys.argv[0]))

        for argument, argument_value in input_arguments_dict.items():
            if argument_value is None:
                self.log.critical(f"Аргумент {argument}, необходимый для данной команды, отсутствует")
                raise KeyError(ERROR_MISSING_ARGS.format(filename=sys.argv[0], command=command))
        self.run_process(command, input_arguments_dict)

if __name__ == "__main__":
    try:
        Facade()
    except BaseException as error:
        print(f"Возникла критическая ошибка: {error}")
        print("\n".join(get_logs()))
        sys.exit(1)
