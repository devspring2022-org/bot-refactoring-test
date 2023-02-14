from .request import Request


class CommonObject():
    def __init__(self,
                 request: Request,
                 url: str,
                 data: dict,
                 restricted: bool = False):
        self._request = request
        self._url = url
        self._data = data
        self._restricted = restricted
        self._fill_attributes()

    def __getitem__(self, key: str):
        if key not in self._config:
            raise KeyError(f"В объекте отсутствует секция '{key}'.")
        return self.data[key]

    def __getattr__(self, name):
        if self._data.get(name) is None and self._restricted:
            self.complete()
            if not hasattr(self, name):
                class_name = self.__class__.__name__
                raise KeyError(f"У класса {class_name} не существует поля {name}")
        return object.__getattribute__(self, name)

    def _fill_attributes(self):
        for key, value in self._data.items():
            setattr(self, key, value)

    def complete(self):
        _, self._data = self._request.request_with_check("GET", self._url)
        self._fill_attributes()
        self._restricted = False
