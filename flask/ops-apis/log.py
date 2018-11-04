import os
import logging
import logging.handlers


def init_log(log_path, logger=None, level=logging.DEBUG, when="D", backup=7,
             format="%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s",
             datefmt="%Y-%m-%d %H:%M:%S"):

    formatter = logging.Formatter(format, datefmt)
    if not logger:
      logger = logging.getLogger()
    logger.setLevel(level)

    directory = os.path.dirname(log_path)
    if not os.path.isdir(directory):
        os.makedirs(directory)

    handler = logging.handlers.TimedRotatingFileHandler(log_path + ".log",
                                                        when=when,
                                                        backupCount=backup)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
