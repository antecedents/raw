"""Module data.py"""
import datetime
import logging
import os

import pandas as pd

import config
import src.functions.streams
import src.source.api
import src.source.inspect


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

        # Configurations
        self.__configurations = config.Config()
        self.__rename = {
            'WeekEndingDate': 'week_ending_date', 'HBT': 'health_board_code', 'TreatmentLocation': 'hospital_code',
            'NumberOfAttendancesEpisode': 'n_attendances', 'NumberWithin4HoursEpisode': 'n_within_4_hours', 
            'NumberOver4HoursEpisode': 'n_over_4_hours', 'NumberOver8HoursEpisode': 'n_over_8_hours', 
            'NumberOver12HoursEpisode': 'n_over_12_hours', 'DepartmentType': 'department_type',
            'AttendanceCategory': 'attendance_category'}

    def __get_data(self) -> pd.DataFrame:
        """

        :return:
        """

        space = '%20'
        string = self.__url + f"&limit=1000000&q='Type{space}1,Unplanned'"
        logging.info(string)

        return src.source.api.API()(url=string)

    def __get_key_fields(self, data: pd.DataFrame):
        """

        :return:
        """

        frame = data.copy()[self.__rename.keys()]
        frame.rename(columns=self.__rename, inplace=True)

        return frame

    @staticmethod
    def __formats(data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        data['week_ending_date'] = pd.to_datetime(
            data['week_ending_date'].astype(dtype=str), errors='coerce', format='%Y%m%d')

        for field in ['department_type', 'attendance_category']:
            data[field] = data[field].str.title()

        return data

    @staticmethod
    def __persist(blob: pd.DataFrame, path: str):
        """

        :param blob: The data being saved.
        :param path: The storage string of a data set.
        :return:
        """

        streams = src.functions.streams.Streams()

        return streams.write(blob=blob, path=path)

    def exc(self) -> None:
        """

        :return:
        """

        data = self.__get_data()

        # Assert
        src.source.inspect.Inspect(data=data).exc()

        # The critical data fields
        data = self.__get_key_fields(data=data.copy())
        frame = self.__formats(data=data.copy())
        logging.info(frame)

        # Date Stamp: The most recent Tuesday.  The code of Tuesday is 1, hence now.weekday() - 1
        now = datetime.datetime.now()
        offset = (now.weekday() - 1) % 7
        tuesday = now - datetime.timedelta(days=offset)
        stamp = tuesday.strftime('%Y-%m-%d')
        logging.info(stamp)

        # Persist
        message = self.__persist(blob=frame, path=os.path.join(self.__configurations.data_, f'{stamp}.csv'))
        logging.info(message)
