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
