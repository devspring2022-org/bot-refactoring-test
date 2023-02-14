from __future__ import annotations


class Monad():
    def __init__(self, expected_result: str or bool, result: str or bool or None = None):
        self.expected_result = expected_result
        if result is None:
            self._result = expected_result
        else:
            self._result = result

    def next(self, function: object, *args, **kwargs) -> Monad:
        if self._result == self.expected_result:
            self._result = function(*args, **kwargs)
        return Monad(self.expected_result, self._result)

    def get_result(self):
        return self._result
