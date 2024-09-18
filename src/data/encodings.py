"""Module encodings.py"""
import typing
import pandas as pd

class Encodings:
    """

    This class enumerates the viable tags, and provides the inverse mappings.
    """

    def __init__(self):
        pass


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

    def __exc(self, elements: pd.DataFrame):
        """

        :param elements: pd.DataFrame: tag | annotation | category
        :return:
        """

        enumerator, archetype = self.__coding(series=elements['tag'])

        return enumerator, archetype
