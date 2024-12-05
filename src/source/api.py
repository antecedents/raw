import urllib.request
import json

import pandas as pd

class API:

    def __init__(self):
        pass

    @staticmethod
    def __get_dictionary(url: str):

        try:
            blob = urllib.request.urlopen(url=url)
        except FileExistsError as err:
            raise err from err

        objects = blob.read()
        dictionary = json.loads(s=objects)

        return dictionary

    @staticmethod
    def __data(dictionary: dict) -> pd.DataFrame:

        try:
            frame = pd.DataFrame.from_dict(data=dictionary['result']['records'], orient='columns')
        except ImportError as err:
            raise err from err

        return frame

    def __call__(self, url: str) -> pd.DataFrame:

        dictionary = self.__get_dictionary(url=url)
        data = self.__data(dictionary=dictionary)

        return data
