"""
Модуль реализация класса - шаблона проектирования "Singleton"
"""


class Singleton(type):
    """
    Класс предназначен для использования шаблона "Singleton".
    Укажите Singleton в параметр metaclass описываемого класса
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
