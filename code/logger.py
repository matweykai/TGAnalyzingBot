import logging
import sys
from bot_configuration import bot_config
from os import path
from datetime import date


class Logger:
    """Singleton logger class"""
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

            if bot_config.logging_path:
                cur_date = date.today()
                handler = logging.FileHandler(path.join('..', bot_config.logging_path,
                                                        f'{cur_date.year}_{cur_date.month}_{cur_date.day}.log'))
            else:
                handler = logging.StreamHandler(sys.stdout)

            # Constructing logger instance
            logger = logging.getLogger()
            handler.setFormatter(logging.Formatter('%(levelname)s::%(asctime)s->%(message)s',
                                                   datefmt='%d/%m/%Y %I:%M:%S'))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

            cls.instance._logger = logger

        return cls.instance._logger
