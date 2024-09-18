"""Module filtering.py"""
import logging

import pandas as pd


class Filtering:

    def __init__(self):
        """

        Constructor
        """

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __call__(self, data: pd.DataFrame, elements: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :param elements:
        :return:
        """

        frame: pd.DataFrame = data.copy().loc[data['category'].isin(values=elements['category'].unique()), :]

        self.__logger.info(frame.head())
        frame.info()

        return frame
