"""Module institutions.py"""
import logging
import os

import numpy as np
import pandas as pd

import config
import src.functions.streams
import src.source.api


class Institutions:
    """
    Notes<br>
    ------<br>

    This class
        <ul>
            <li>Retrieves and saves the latest raw institutions/hospitals data.</li>
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
        logging.info(self.__data)

        self.__rename = {'HospitalCode': 'hospital_code', 'HospitalName': 'hospital_name',
                         'AddressLine1': 'address_line_1', 'AddressLine2': 'address_line_2',
                         'AddressLine3': 'address_line_3', 'AddressLine4': 'address_line_4',
                         'Postcode': 'post_code', 'HealthBoard': 'health_board_code', 'HSCP': 'hscp_code',
                         'CouncilArea': 'council_area', 'IntermediateZone': 'intermediate_zone',
                         'DataZone': 'data_zone'}

    def __inspect(self, field: str):
        """
        This function checks whether a specified field has distinct values.

        :param field: A field of interest
        :return:
        """

        tensor: np.ndarray = self.__data[field].unique()

        assert tensor.shape[0] == self.__data[field].shape[0], f'The {field} field values are not distinct.'

    def __get_key_fields(self) -> pd.DataFrame:
        """

        :return:
        """

        frame = self.__data.copy()[self.__rename.keys()]
        frame.rename(columns=self.__rename, inplace=True)

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
        self.__inspect(field='HospitalCode')

        # The critical data fields
        frame = self.__get_key_fields()

        # Persist: Raw
        message = self.__persist(blob=self.__data, path=os.path.join(self.__configurations.parent_, 'raw', 'references', 'institutions.csv'))
        logging.info(message)

        # Persist: Critical Fields
        message = self.__persist(blob=frame, path=os.path.join(self.__configurations.parent_, 'latest', 'references', 'institutions.csv'))
        logging.info(message)

