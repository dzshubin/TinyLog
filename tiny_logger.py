
import json
import logging.config


class ConsoleFilter(logging.Filter):
    '''标准输出过滤器

    该过滤器附加在Logger或者Handler(默认)上，使用用户设置
    的参数，决定是否将log输出在stderr或者stdout上。
    '''

    def __init__(self, print2console=0):
        self.flag = print2console

    def filter(self, record):
        '''过滤函数

        在Logger或者Handler之前调用，决定是否输出在stderr或者stdout上

        Params:
            record: log消息体

        Returns: 返回是否进一步处理。True即进一步处理消息。
        '''
        if self.flag == 1:
            return True
        else:
            return False


def setup():
    try:
        fp = open('logging.json')
        d = json.load(fp)
        logging.config.dictConfig(d)

    except OSError as oe:
        # 文件不能打开
        return 0
    except FileExistsError as fee:
        # 以独占模式打开文件，但是文件已经存在
        return 0
    finally:
        fp.close()
        return 1