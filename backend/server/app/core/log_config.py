import os
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
import datetime
import json
os.makedirs(f"{os.getcwd()}/logs", exist_ok=True)

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BaseLogger(metaclass=SingletonMeta):

    def __init__(self):
        self.__logger = self.set_logger()

    # def __call__(self, *args, **kwargs):
    #     print(f"{type(self).__name__} is called!!")

    def info(self, msg):
        self.__logger.info(msg=msg)

    def set_logger(self):
        logger = logging.getLogger(type(self).__name__)

        # set Log Level
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        #add stream handler
        stream_formatter = jsonlogger.JsonFormatter(fmt='%(threadName)s %(process)d %(asctime)s %(message)s ',json_ensure_ascii=False)
        ch.setFormatter(stream_formatter)
        logger.addHandler(ch)

        # set FIle Handler
        log_file_path = os.path.join(os.getcwd(),"logs","dummy.log")
        fh = RotatingFileHandler(filename=log_file_path,maxBytes=10000,backupCount=0,encoding='utf-8')
        fh.setLevel(logging.INFO)

        file_formatter = jsonlogger.JsonFormatter(fmt='%(threadName)s %(process)d %(asctime)s %(message)s',json_ensure_ascii=False)
        fh.setFormatter(file_formatter)
        logger.addHandler(fh)


        return logger


base_logger = BaseLogger()


# class BaseLogger(metaclass=SingletonMeta):
#
#     def __init__(self):
#         self.__logger = self.set_logger()
#
#     # def __call__(self, *args, **kwargs):
#     #     print(f"{type(self).__name__} is called!!")
#
#     def info(self, msg):
#         self.__logger.info(msg=msg)
#
#     def set_logger(self):
#         logger = logging.getLogger(type(self).__name__)
#
#         # set Log Level
#         logger.setLevel(logging.INFO)
#         # set Stream Handle
#         ch = logging.StreamHandler()
#         ch.encoding = 'utf-8'
#         ch.setLevel(logging.INFO)
#         stream_formatter = logging_json.JSONFormatter(fields={
#             "name": "name",
#             "level_name": "levelname",
#             "thread": "thread",
#             "process": "process",
#             "response": "response"
#         })
#         ch.setFormatter(stream_formatter)
#         logger.addHandler(ch)
#         # set Formatter
#         file_formatter = logging_json.JSONFormatter(fields={
#             "name": "name",
#             "level_name": "levelname",
#             "thread": "thread",
#             "thread_name": "threadName",
#             "process": "process",
#             "process_name": "processName",
#             "response":"response"
#         })
#
#         file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#
#         # set File Handler
#
#         fh = logging.FileHandler(filename=f"{os.getcwd()}/logs/dummy.log",encoding='utf-8')
#         fh.setFormatter(file_formatter)
#         fh.setLevel(logging.INFO)
#         logger.addHandler(fh)
#         return logger