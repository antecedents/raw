"""Module objects.py"""
import logging
import typing

import pandas as pd

import src.data.source
import src.data.tags
import src.data.specimens

class Objects:

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

    def tags(self, blob: pd.DataFrame) -> pd.DataFrame:
        """
        The viable/applicable tags

        :param blob:
        :return:
        """

        elements = src.data.tags.Tags(data=blob).exc()
        self.__logger.info(elements)

        return elements

    def data(self) -> pd.DataFrame:
        """

        :return:
        """

        # The raw data
        data = self.__raw()

        # The viable tags, etc.
        elements = self.tags(blob=data)

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

        return frame
