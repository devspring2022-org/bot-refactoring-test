import logging


LOGS = []


def common_log(cls=None, *, name=""):
    class VariablesExpansionFilter(logging.Filter):
        def filter(self, record):
            record.caller = f"{record.filename} -> {record.name} -> {record.funcName}"
            record.space = " "
            return True

    class LogSavingHandler(logging.StreamHandler):
        def __init__(self):
            logging.StreamHandler.__init__(self)
            format = ("[{levelname:^10}] From: {caller}\n"
                      "{space:<12} {message}")
            formatter = logging.Formatter(format, style="{")
            self.setFormatter(formatter)

        def emit(self, record):
            LOGS.append(self.format(record))

    def wrapper(cls):
        cls.log = logging.getLogger(name or cls.__name__)
        cls.log.addFilter(VariablesExpansionFilter())
        cls.log.setLevel(logging.INFO)
        if not cls.log.handlers:
            cls.log.addHandler(LogSavingHandler())
        return cls

    return wrapper(cls) if cls else wrapper

def get_logs():
    return LOGS
