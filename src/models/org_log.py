"""
Log setting model
"""
import dataclasses
import json
import os
import logging
import logging.config


@dataclasses.dataclass
class OrgLog:
    """ Log setting model """

    def __init__(self, conf_file='conf/log_format.json', logger_name=None):
        if not os.path.isdir('../log'):
            os.makedirs('../log', exist_ok=True)
        self._read_conf_file(conf_file)
        self.logger = logging.getLogger(logger_name)

    @classmethod
    def _read_conf_file(cls, conf_file: str):
        """ Loading a format file """
        with open(conf_file, 'r', encoding='utf-8') as conf_f:
            conf_file = json.load(conf_f)
            logging.config.dictConfig(conf_file)

    def _test(self):
        """ Test Run """
        self._read_conf_file(conf_file='../conf/log_format.json')
        self.logger.info('test info')
        self.logger.error('test error')
