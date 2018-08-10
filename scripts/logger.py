# coding: utf-8
import logging


class Logger:
    def __init__(self, path, level=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(level)
        fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(filename)s[%(lineno)d] %(message)s', '%Y-%m-%d %H:%M:%S')
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(level)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warnning(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    logger = Logger('aap.log', logging.ERROR)
    logger.error('hahaha error msg')
