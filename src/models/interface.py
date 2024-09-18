"""Module interface.py"""
import logging

import pandas as pd

import src.data.splittings
import src.elements.frames as fra


class Interface:
    """
    Interface: Models
    """

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        splittings: fra.Frames = src.data.splittings.Splittings(data=data).exc()

        # Logging
        logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)


    def exc(self, architecture: str):
        """

        :param architecture:
        :return:
        """

        match architecture:
            case 'bert':
                self.__logger.info('...')
            case 'distil':
                self.__logger.info('...')
            case 'electra':
                self.__logger.info('...')
            case _:
                self.__logger.info('?')
