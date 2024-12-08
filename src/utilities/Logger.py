import simpy


class Logger:
    instance: "Logger" = None

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

    def log(self, msg):
        print(f'[{self.env.now:.2f}] {msg}')
