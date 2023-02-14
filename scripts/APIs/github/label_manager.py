from github.Label import Label
from github.Repository import Repository


class LabelData:
    def __init__(self, name: str, color: str, description: str):
        self.name = name
        self.color = color
        self.description = description


class LabelManager:
    """
    Данный класс предназначен для работы с метками GitHub.
    """
    _AVAILABLE_LABELS = {
        '3': LabelData('3', '2bd600', '3 балла'),
        '2': LabelData('2', 'b4fb11', '2 балла'),
        '1': LabelData('1', 'f0c205', '1 балл'),
        'passed': LabelData('passed', '008000', 'Проверка пройдена'),
        'failed': LabelData('failed', '990000', 'Проверка провалена'),
        'violated': LabelData('violated', '800080', 'Проверка провалена, PR закрыт'),
        'deadline-': LabelData('deadline-', '383838', 'PR открыт после дедлайна'),
        'unauthorized-merge': LabelData('unauthorized-merge', 'ff0000', 'Несанкционированный мердж PR'),
        'report ok': LabelData('report ok', 'A3F162', 'Проверка отчета пройдена'),
        'report failed': LabelData('report failed', 'EE2D1A', 'Проверка отчета провалена'),
        '-1': LabelData('-1', '6f17c7', '-1 балл'),
        "moodle+": LabelData('moodle+', 'dec24c', 'Работа выполнена на moodle'),
        "teacher approval": LabelData("teacher approval", "b39cde", "Проверено преподавателем")
    }
    
    GRADES_LABELS = ['1', '2', '3']

    def __init__(self, repository: Repository):
        self._repository = repository

    def get_label(self, name: str) -> Label or None:
        if name.lower() not in self._AVAILABLE_LABELS.keys():
            return None

        repository_label = self._get_repository_label_if_already_exist(name)
        if repository_label is not None:
            return repository_label

        label_data = self._AVAILABLE_LABELS[name]
        return self._repository.create_label(label_data.name, label_data.color, label_data.description)

    def add_label_to_pull_request(self, pr_number: int, label_name: str) -> None:
        label = self.get_label(label_name)
        if label is not None:
            self._repository.get_pull(pr_number).add_to_labels(label)

    def remove_label_from_pull_request(self, pr_number: int, label_name: str) -> None:
        label = self.get_pull_request_label_if_already_added(pr_number, label_name)
        if label is not None:
            self._repository.get_pull(pr_number).remove_from_labels(label)

    def get_pull_request_label_if_already_added(self, pr_number: int, label_name: str) -> Label or None:
        labels_paginated_list = self._repository.get_pull(pr_number).get_labels()
        for label in labels_paginated_list:
            if label.name == label_name:
                return label
        return None

    def _get_repository_label_if_already_exist(self, label_name: str) -> Label or None:
        repository_labels = self._repository.get_labels()
        for label in repository_labels:
            if label.name.lower() == label_name.lower():
                return label
        return None

    def remove_another_grades_labels(self, grade_label: str, pr_number: int) -> None:
        for label in self.GRADES_LABELS:
            if label != grade_label:
                self.remove_label_from_pull_request(pr_number, label)
