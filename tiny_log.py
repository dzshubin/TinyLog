import logging.config



class ConsoleFilter(logging.Filter):
    '''标准输出过滤器
    
    该过滤器附加在Logger或者Handler(默认)上，使用用户设置
    的参数，决定是否将log输出在stderr或者stdout上。
    '''

    def __init__(self, param=0):
        self.param = param

    def filter(self, record):
        '''过滤函数
        
        在Logger或者Handler之前调用，决定是否输出在stderr或者stdout上
                
        Params:
            record: log消息体
        
        Returns: 返回是否进一步处理。True即进一步处理消息。
        '''
        if self.param == 1:
            return True
        else:
            return False




