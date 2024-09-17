"""Module interface.py"""
import logging
import typing

import pandas as pd

import src.data.splittings


class Interface:
    """
    Interface
    """

    def __init__(self, frame: pd.DataFrame):
        """

        :param frame:
        """

        self.__frame = frame

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger(__name__)

    def __splits(self):

        training, validating, testing = src.data.splittings.Splittings(
            frame=self.__frame).exc()
        training.info()
        validating.info()
        testing.info()


    def get_datasets(self):
        pass

    def get_rays(self):
        pass
