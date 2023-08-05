# -*- coding: utf-8 -*-

"""
this is a simple logger for python

logger's level as :

0 - NOTSET
1 - DEBUG
2 - INFO
3 - WARNING
4 - ERROR
5 - CRITICAL
"""

import logging
import os
import shutil
import time

__version__ = '0.0.2'
__license__ = 'MIT'
__author__ = 'Jeffrey Zhang'

loger_level = {
    5: logging.CRITICAL,
    4: logging.ERROR,
    3: logging.WARNING,
    2: logging.INFO,
    1: logging.DEBUG,
    0: logging.NOTSET
}


def create_logger(logname='pyselog', fileloglevel=False, streamloglevel=2, file_folder='%s_logs',
                  delete_existed_file=False):
    file_create = True
    warning_msg = None

    rl = logging.getLogger(logname)
    rl.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(pathname)s(line %(lineno)d) - %(name)s.%(levelname)s - : %(message)s')

    if fileloglevel:
        if file_folder == '%s_logs':
            file_folder = file_folder % logname
            file_folder = os.path.join(os.getcwd(), file_folder)

        try:
            if os.path.exists(file_folder):
                if delete_existed_file:
                    shutil.rmtree(file_folder)
                    os.mkdir(file_folder)
            else:
                os.mkdir(file_folder)

            fh = logging.FileHandler('%s/%s_%s.log' % (file_folder, logname, time.strftime('%Y-%m-%d')))
            fh.setLevel(loger_level[fileloglevel])
            fh.setFormatter(formatter)
            rl.addHandler(fh)
        except FileNotFoundError as e:
            warning_msg = e
            file_create = False

    if streamloglevel:
        sh = logging.StreamHandler()
        sh.setLevel(loger_level[streamloglevel])
        sh.setFormatter(formatter)
        rl.addHandler(sh)

    if not file_create:
        rl.warning('>>> file logger create defeated <<< %s' % warning_msg)

    return rl


if __name__ == '__main__':
    logger_object = create_logger()
    logger_object.info('info message')
    logger_object.error('error message')
