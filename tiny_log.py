import logging.config



class ConsoleFilter(logging.Filter):
    def __init__(self, param=0):
        self.param = param

    def filter(self, record):
        if self.param == 1:
            return True
        else:
            return False




