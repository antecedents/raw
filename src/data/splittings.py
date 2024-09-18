"""Module splittings.py"""
import logging
import typing

import pandas as pd

import config
import src.elements.frames as fra


class Splittings:
    """
    Splits a dataframe into training, validating, and testing parts.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        """

        :param data: The data set for the modelling stages
        """

        self.__data: pd.DataFrame = data

        # Configurations
        self.__configurations = config.Config()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __split(self, data: pd.DataFrame, frac: float) -> typing.Tuple[pd.DataFrame, pd.DataFrame]:
        """
        This method splits  data set into parent & child data sets.

        :return:
        parent : pandas.DataFrame<br>
            The data set for parent<br>
        child : pandas.DataFrame<br>
            The data set for the child stage
        """

        blob = data.copy()

        parent = blob.sample(frac=frac, random_state=self.__configurations.seed)
        child = blob.drop(parent.index)

        parent.reset_index(drop=True, inplace=True)
        child.reset_index(drop=True, inplace=True)

        return parent, child

    def exc(self, f_training: float = 0.8, f_validating: float = 0.9) -> fra.Frames:
        """

        :param f_training: If there are N instances, [f_training * N] instances are set aside for training.<br>
        :param f_validating:<br>
               * If f_validating less than 1.0,  [f_validating * (1 - f_training) * N] instances are set aside
                 for validating, and [(1 - f_validating) * (1 - f_training) * N] for testing.<br>
               * Otherwise, if f_validating = 1.0, [(1 - f_training) * N] instances are set aside for
                 validating
        :return:
            src.elements.frames.Frames(
                training: pandas.DataFrame, validating: pandas.DataFrame, testing: pandas.DataFrame)
        """

        training, validating = self.__split(data=self.__data, frac=f_training)

        if f_validating < 1.0:
            validating, testing = self.__split(data=validating, frac=f_validating)
        else:
            testing = None

        frames = fra.Frames(
            training=training, validating=validating, testing=testing)

        return frames
