"""Module boards.py"""
import logging
import os

import numpy as np
import pandas as pd

import config
import src.functions.streams
import src.source.api


class Boards:

    def __init__(self, url: str) -> None:
        """

        :param url: The uniform resource locator of the data
        """

        self.__url = url

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

        # Data
        self.__data = src.source.api.API().__call__(url=self.__url)
        self.__data.info()
        logging.info(self.__data)

        self.__rename = {'HB': 'health_board_code', 'HBName': 'health_board_name',
                         'HBDateEnacted': 'health_board_date_enacted'}

    def __inspect(self, field: str, expectation: int):
        """
        This function checks whether a specified field has the expected number of distinct values.

        :param field: A field of interest
        :param expectation: The expected number of elements
        :return:
        """

        tensor: np.ndarray = self.__data[field].unique()

        assert tensor.shape[0] == expectation, f'The number of distinct {field} values is not equal to {expectation}'

    def __get_key_fields(self):
        """

        :return:
        """

        frame = self.__data.copy()[self.__rename.keys()]
        frame.rename(columns=self.__rename, inplace=True)
        frame['health_board_date_enacted'] = pd.to_datetime(
            frame['health_board_date_enacted'].astype(dtype=str), errors='coerce', format='%Y%m%d')

        return frame

    def __persist(self, blob: pd.DataFrame, path: str):
        """

        :param blob: The data being saved.
        :param path: The storage string of a data set.
        :return:
        """

        return self.__streams.write(blob=blob, path=path)

    def exc(self) -> None:
        """

        :return:
        """


        # Assert
        self.__inspect(field='HB', expectation=self.__data.shape[0])
        self.__inspect(field='Country', expectation=1)

        # The critical data fields
        frame = self.__get_key_fields()

        # Persist: Raw
        message = self.__persist(blob=self.__data, path=os.path.join(self.__configurations.parent_, 'raw', 'references', 'boards.csv'))
        logging.info(message)

        # Persist: Critical Fields
        message = self.__persist(blob=frame, path=os.path.join(self.__configurations.parent_, 'latest', 'references', 'boards.csv'))
        logging.info(message)
