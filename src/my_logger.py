import logging
import os
import sys


def setup_logger():
    """Установка своего логгера"""
    logger = logging.getLogger('casino_logger')
    logger.setLevel(logging.INFO)

    logger.propagate = False

    path_casino_log = os.path.abspath(os.path.join(os.path.dirname(__file__), 'casino.log'))

    file_handler = logging.FileHandler(path_casino_log, mode='a')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt='[ %(asctime)s ] %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    console_formatter = logging.Formatter(
        '%(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
