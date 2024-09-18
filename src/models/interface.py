"""Module interface.py"""
import logging

import pandas as pd

import src.data.interface


class Interface:
    """
    Interface: Models
    """

    def __init__(self, specimens: pd.DataFrame):
        """

        :param specimens:
        """

        self.__specimens: pd.DataFrame = specimens

        # An instance for retrieving the train/validate/test splits of the data.  The methods
        # deliver datasets.DatasetDict or dict[str, ray.data.dataset.MaterializedDataset]
        self.__api = src.data.interface.Interface(data=self.__specimens)

        # Logging
        logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)


    def exc(self):
        """

        :return:
        """

        data = self.__api.get_rays()

        self.__logger.info(type(data))
        self.__logger.info(data.keys())
