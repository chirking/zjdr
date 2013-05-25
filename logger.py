#coding=utf-8

import logging
import sys

sys.path.append(".")
import env

# create logger with 'zjdr'
logger = logging.getLogger('zjdr')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler(env.logger_path+'zjdr.log')
fh.setLevel(logging.WARN)

# create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
# logger.addHandler(ch)


logger.warn('init logger zjdr: '+str(logger))