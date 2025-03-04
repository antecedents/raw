"""Module viable.py"""
import logging
import os

import numpy as np
import pandas as pd

import config
import src.functions.streams


class Viable:
    """
    Retains the institutions/hospitals that have a viable number of observations.
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: The set of modelling & decomposition arguments, vis-à-vis forecasting
                          algorithm and supplements.
        """

        self.__arguments = arguments

        # Instance
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

    def __codes(self, blob: pd.DataFrame) -> np.ndarray:
        """

        :param blob:
        :return:
        """

        # Counts per institution
        counts: pd.DataFrame = blob.copy()[['health_board_code', 'hospital_code']].groupby(
            by='health_board_code').value_counts().to_frame()
        counts.reset_index(inplace=True)

        # Institutions that have a viable number of observations.
        viable: pd.DataFrame = counts.loc[counts['count'] >= (
                self.__arguments.get('seasons') * self.__arguments.get('cycles')), :]

        return viable['hospital_code'].to_numpy()

    def exc(self, data: pd.DataFrame):
        """

        :param data: The raw data.
        :return:
        """

        codes = self.__codes(blob=data)
        frame = data.copy().loc[data['hospital_code'].isin(codes), self.__configurations.fields]

        # Persist
        message = self.__streams.write(
            blob=frame,
            path=os.path.join(self.__configurations.modelling_, f'{self.__configurations.stamp}.csv'))
        logging.info('VIABLE -> %s', message)
