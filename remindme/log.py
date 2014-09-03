# -*- coding: UTF-8 -*-

# see http://sametmax.com/ecrire-des-logs-en-python/ (FR)

import logging
from logging.handlers import RotatingFileHandler

def mkLogger(name, level=logging.DEBUG):
    if not name.startswith('remindme'):
        name = 'remindme.%s' % name

    output = '%s.log' % name

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    file_handler = RotatingFileHandler(output, 'a', 1000000, 1)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = mkLogger('remindme')  # generic logger
