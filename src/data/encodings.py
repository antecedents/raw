"""Module encodings.py"""
import logging
import typing

import pandas as pd


class Encodings:
    """

    This class enumerates the viable tags, and provides the inverse mappings.
    """

    def __init__(self):
        """
        Constructor
        """

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)


    @staticmethod
    def __coding(series: pd.Series) -> typing.Tuple[dict, dict]:
        """
        Tags enumeration, and their inverse mappings.

        :param series:
        :return:
        """

        enumerator = {k: v for v, k in enumerate(iterable=series)}

        archetype = {v: k for v, k in enumerate(iterable=series)}

        return enumerator, archetype

    def exc(self, elements: pd.DataFrame) -> typing.Tuple[dict, dict]:
        """

        :param elements: pd.DataFrame: tag | annotation | category
        :return:
        """

        enumerator, archetype = self.__coding(series=elements['tag'])
        self.__logger.info(enumerator)
        self.__logger.info(archetype)

        return enumerator, archetype
