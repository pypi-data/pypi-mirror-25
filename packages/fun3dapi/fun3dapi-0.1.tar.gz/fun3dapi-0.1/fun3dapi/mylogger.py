import logging
import tornado.log

def mylogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    if not len(logger.handlers):
        fileHandler = logging.FileHandler('/home/john/' + name + '.log')
        fileHandler.setFormatter(tornado.log.LogFormatter())
        logger.addHandler(fileHandler)
    return logger
