import logging
from logging import handlers


class Logger(object):
    kv = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=7,
            fmt='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s'):
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(self.kv.get(level))
        fmt_str = logging.Formatter(fmt)

        sh = logging.StreamHandler()  # 标准输出
        sh.setFormatter(fmt_str)

        fh = handlers.TimedRotatingFileHandler(filename=filename,
                when=when, backupCount=backCount, encoding='utf-8')
        fh.setFormatter(fmt_str)

        self.logger.addHandler(sh)
        self.logger.addHandler(fh)


log = Logger('app.log', level='debug').logger


class Student(object):
    def __init__(self, name):
        self.name = name

    @property
    def socre(self):
        return self.__score

    @socre.setter
    def score(self, score):
        if isinstance(score, int):
            self.__score = score
            log.info(f'name: {self.name}, score: {score}')
        else:
            log.error(f'student\'s score is not type of int. {str(type(score))}.')
            raise TypeError(f'the type of score is {str(type(score))}, not int.')


if __name__ == "__main__":
    zhangsan = Student('zhangsan')
    zhangsan.score = 90
    wangwu = Student('wangwu')
    wangwu.score = 86.5
