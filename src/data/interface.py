"""Module interface.py"""
import logging
import typing

import pandas as pd

import src.data.source
import src.data.tags
import src.data.specimens
import src.data.splittings


class Interface:
    """
    Interface
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

    def __raw(self) -> pd.DataFrame:
        """
        The raw data

        :return:
        """

        data: pd.DataFrame = src.data.source.Source().exc()
        self.__logger.info(data)

        return data

    def __tags(self, data: pd.DataFrame) -> typing.Tuple[pd.DataFrame, dict, dict]:
        """
        The viable tags, and the corresponding tags enumerator & archetype

        :param data:
        :return:
        """

        elements, enumerator, archetype = src.data.tags.Tags(data=data).exc()
        self.__logger.info(elements)
        self.__logger.info(enumerator)
        self.__logger.info(archetype)

        return elements, enumerator, archetype

    def exc(self):
        """

        :return:
        """

        # The raw data
        data = self.__raw()

        # The viable tags, etc.
        elements, enumerator, archetype = self.__tags(data=data)

        # The viable data instances vis-à-vis viable tags
        data: pd.DataFrame = data.copy().loc[data['category'].isin(values=elements['category'].unique()), :]
        self.__logger.info(data.head())
        data.info()

        # Hence, the expected structure.  Within the preceding dataframe each distinct sentence
        # is split across rows; a word per row, in order.  The Specimen class re-constructs the
        # original sentences.
        frame: pd.DataFrame = src.data.specimens.Specimens(data=data).exc()
        self.__logger.info(frame.head())
        frame.info()

        training, validating, testing = src.data.splittings.Splittings(
            frame=frame).exc()
        training.info()
        validating.info()
        testing.info()
