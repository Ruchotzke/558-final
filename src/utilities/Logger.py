from enum import Enum

import simpy


class Level(Enum):
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4
    TRACE = 5

class Logger:
    instance: "Logger" = None
    LOG_LEVEL = Level.TRACE

    def __new__(cls, *args, **kwargs):
        """
        Singleton constructor
        :param args:
        :param kwargs:
        """
        if cls.instance is None:
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    def init_instance(self, env: simpy.Environment):
        """
        Initialize the instance.
        :param env:
        :return:
        """
        self.env = env

    def log(self, log_level: Level, msg):
        if self.LOG_LEVEL.value >= log_level.value:
            print(f'[{self.env.now:.2f}] {msg}')
