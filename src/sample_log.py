import configparser
import json
import logging
import uuid

import os
from logging import StreamHandler, FileHandler, Formatter
from logging import INFO, DEBUG, NOTSET

import logging.config

_EXEC_FILE_NAME = os.path.basename(__file__)[:-3]


def read_conf_file(conf_file: str):
    """ Loading a format file """
    with open(conf_file, 'r', encoding='utf-8') as f:
        f_ = json.load(f)
        logging.config.dictConfig(f_)


def get_logger(logger_='simpleDefault'):
    """ ロガー生成 """
    return logging.getLogger(logger_)


def test():
    """ Run """
    read_conf_file(conf_file='conf/log_format.json')

    # 指定 logger名
    logger = get_logger(logger_=_EXEC_FILE_NAME)
    logger.info('test info')
    logger.error('test error')


if __name__ == '__main__':
    test()
