"""Module data.py"""
import datetime
import logging
import os

import numpy as np
import pandas as pd

import config
import src.functions.streams
import src.source.api


class Data:
    """
    Notes<br>
    ------<br>

    This class
        <ul>
            <li>Retrieves and saves the current version of the raw data.</li>
            <li>Extracts and structures the relevant fields for modelling & analysis; subsequently saves.</li>
        </ul>
    """

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

        self.__rename = {
            'WeekEndingDate': 'week_ending_date', 'HBT': 'health_board_code', 'TreatmentLocation': 'hospital_code',
            'NumberOfAttendancesEpisode': 'n_attendances', 'NumberWithin4HoursEpisode': 'n_within_4_hours', 
            'NumberOver4HoursEpisode': 'n_over_4_hours', 'NumberOver8HoursEpisode': 'n_over_8_hours', 
            'NumberOver12HoursEpisode': 'n_over_12_hours'}

    def __inspect(self, field: str):
        """
        This function checks whether a specified field has a single distinct value only.

        :param field: A field of interest
        :return:
        """

        tensor: np.ndarray = self.__data[field].unique()

        assert tensor.shape[0] == 1, f'The number of distinct {field} values is > 1.'

    def __get_key_fields(self):
        """

        :return:
        """

        frame = self.__data.copy()[self.__rename.keys()]
        frame.rename(columns=self.__rename, inplace=True)
        frame['week_ending_date'] = pd.to_datetime(
            frame['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y%m%d')

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
        self.__inspect(field='DepartmentType')
        self.__inspect(field='Country')

        # The critical data fields
        frame = self.__get_key_fields()

        # Persist: Raw
        stamp = datetime.datetime.now().strftime('%Y-%m-%d')
        message = self.__persist(blob=self.__data, path=os.path.join(self.__configurations.parent_, 'raw', 'data', f'{stamp}.csv'))
        logging.info(message)

        # Persist: Critical Fields
        message = self.__persist(blob=frame, path=os.path.join(self.__configurations.parent_, 'latest', 'data', 'data.csv'))
        logging.info(message)
