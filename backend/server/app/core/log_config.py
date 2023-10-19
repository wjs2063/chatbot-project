import os
import logging
import logging_json
os.makedirs(f"{os.getcwd()}/logs",exist_ok=True)

class BaseLogger:

    def __init__(self):
        self.__logger = self.set_logger()

    def __call__(self, *args, **kwargs):
        print(f"{type(self).__name__} is called!!")

    def info(self,msg):
        self.__logger.info(msg = msg)

    def set_logger(self):
        logger = logging.getLogger(type(self).__name__)
        # set Log Level
        logger.setLevel(logging.INFO)
        # set Stream Handle
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        stream_formatter = logging_json.JSONFormatter(fields={
            "name" : "name",
            "level_name" : "levelname",
            "thread" : "thread",
            "process" : "process"
        })
        ch.setFormatter(stream_formatter)
        logger.addHandler(ch)
        # set Formatter
        file_formatter = logging_json.JSONFormatter(fields={
            "name": "name",
            "level_name": "levelname",
            "thread": "thread",
            "thread_name": "threadName",
            "process": "process",
            "process_name": "processName"
        })

        # set File Handler

        fh = logging.FileHandler(filename=f"{os.getcwd()}/logs/dummy.log")
        fh.setFormatter(file_formatter)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
        return logger

base_logger = BaseLogger()