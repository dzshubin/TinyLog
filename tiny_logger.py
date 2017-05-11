
import json
import os
import time
import logging.config


class ConsoleFilter(logging.Filter):
    """标准输出过滤器

    该过滤器附加在Logger或者Handler(默认)上，使用用户设置
    的参数，决定是否将log输出在stderr或者stdout上。
    """

    def __init__(self, print2console=0):
        self.flag = print2console

    def filter(self, record):
        """过滤函数

        在Logger或者Handler之前调用，决定是否输出在stderr或者stdout上

        Params: record: log消息体

        Returns: 返回是否进一步处理。True即进一步处理消息。
        """
        if self.flag == 1:
            return True
        else:
            return False


class SafeFileHandler(logging.FileHandler):
    """进程安全的按时间切割日志的handler类
    
    Handler在发生消息出去之前，先检查是否需要创建新文件，然后再进行emit操作。
    
    """
    def __init__(self, filename, mode='a', encoding=None, delay=1):
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)
        self.mode = mode
        self.encoding = encoding
        self.suffix = "%Y-%m-%d"
        self.suffix_time = ""

    def emit(self, record):
        try:
            if self.check_basefilename(record):
                self.build_basefilename()
                logging.FileHandler.emit(self, record)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def check_basefilename(self, record):
        """检查是否需要重新创建文件
        
        Params: record: 消息记录
        Returns: 是否需要创建新文件。1-需要
        """
        timeTuple = time.localtime()

        if (self.suffix_time != time.strftime(self.suffix, timeTuple)  # 当前时间戳与当前写入文件的时间戳不同
            or not os.path.exists(self.baseFilename+'.'+self.suffix_time)):  # 后缀为当前时间戳的文件不存在
            return 1
        else:
            return 0

    def build_basefilename(self):
        """创建新的文件
         
        当时间戳过时之后，根据当前时间戳构建新的log文件
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # 删除旧的后缀名
        if self.suffix_time != "":
            index = self.baseFilename.find("."+self.suffix_time)
            if index == -1:
                index = self.baseFilename.rfind(".")
            self.baseFilename = self.baseFilename[:index]

        # 添加新的后缀名
        currentTimeTuple = time.localtime()
        self.suffix_time = time.strftime(self.suffix, currentTimeTuple)
        self.baseFilename += "." + self.suffix_time

        #self.mode = 'a'
        #if not self.delay:
        #    self.stream = self._open()


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