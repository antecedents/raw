"""Module interface.py"""
import logging

import pandas as pd

import src.data.source
import src.data.tags


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

    def exc(self):
        """

        :return:
        """

        # The raw data
        data: pd.DataFrame = src.data.source.Source().exc()
        self.__logger.info(data.head())
        data.info()

        # The viable tags, and the corresponding tags enumerator & archetype
        elements, enumerator, archetype = src.data.tags.Tags(data=data).exc()
        self.__logger.info(elements)
        self.__logger.info(enumerator)
        self.__logger.info(archetype)

        # The viable data instances vis-à-vis viable tags
        data = data.copy().loc[data['category'].isin(values=elements['category'].unique()), :]
        self.__logger.info(data.head())
        data.info()


