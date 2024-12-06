"""Module api.py"""
import json
import urllib.request

import pandas as pd


class API:
    """
    Notes<br>
    ------<br>

    For reading data sets from Scottish Health & Social Care <a href="https://www.opendata.nhs.scot" target="_blank">
    Open Data Platform</a>
    """

    def __init__(self):
        pass

    @staticmethod
    def __get_dictionary(url: str):
        """

        :param url: An application programming interface endpoint
        :return:
        """

        with urllib.request.urlopen(url=url) as blob:
            objects = blob.read()
        dictionary = json.loads(s=objects)

        return dictionary

    @staticmethod
    def __data(dictionary: dict) -> pd.DataFrame:
        """

        :param dictionary: An API (application programming interface) query output.
        :return:
        """

        try:
            frame = pd.DataFrame.from_dict(data=dictionary['result']['records'], orient='columns')
        except ImportError as err:
            raise err from err

        return frame

    def __call__(self, url: str) -> pd.DataFrame:
        """

        :param url: An application programming interface endpoint
        :return:
        """

        dictionary = self.__get_dictionary(url=url)
        data = self.__data(dictionary=dictionary)

        return data
