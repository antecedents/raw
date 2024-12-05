import logging
import datetime
import os

import numpy as np
import pandas as pd

import config
import src.functions.streams
import src.source.api


class Data:

    def __init__(self, url: str) -> None:
        
        self.__url = url

        # Instances
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

        # Data
        self.__data = src.source.api.API().__call__(url=self.__url)
        self.__data.info()

        self.__rename = {
            'WeekEndingDate': 'week_ending_date', 'HBT': 'health_board_code', 'TreatmentLocation': 'treatment_location', 
            'NumberOfAttendancesEpisode': 'n_attendances', 'NumberWithin4HoursEpisode': 'n_within_4_hours', 
            'NumberOver4HoursEpisode': 'n_over_4_hours', 'NumberOver8HoursEpisode': 'n_over_8_hours', 
            'NumberOver12HoursEpisode': 'n_over_12_hours'}

    def __inspect(self, field: str):

        tensor: np.ndarray = self.__data[field].unique()

        assert tensor.shape[0] == 1, f'The number of distinct {field} values is > 1'

    def __get_key_fields(self):

        frame = self.__data.copy()[self.__rename.keys()]
        frame.rename(columns=self.__rename, inplace=True)
        frame['week_ending_date'] = pd.to_datetime(
            frame['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y%m%d')

        return frame

    def __persist(self, blob: pd.DataFrame, path: str):

        return self.__streams.write(blob=blob, path=path)

    def exc(self):


        # Assert
        self.__inspect(field='DepartmentType')
        self.__inspect(field='Country')

        # The critical data fields
        frame = self.__get_key_fields()

        # Persist
        stamp = datetime.datetime.now().strftime('%Y-%m-%d')
        self.__persist(blob=self.__data, path=os.path.join(self.__configurations.parent_, 'raw', 'data', f'{stamp}.csv'))
        self.__persist(blob=frame, path=os.path.join(self.__configurations.parent_, 'latest', 'data', 'data.csv'))

        return
