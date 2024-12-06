import logging
import os

import numpy as np
import pandas as pd

import config
import src.functions.streams
import src.source.api

class Institutions:

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
                         'PostCode': 'post_code', 'HealthBoard': 'health_board_code', 'HSCP': 'hscp_code',
                         'CouncilArea': 'council_area', 'IntermediateZone': 'intermediate_zone',
                         'DataZone': 'data_zone'}
