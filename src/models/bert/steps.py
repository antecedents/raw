"""Module steps.py"""
import logging

import ray.data.dataset

import src.elements.variable as vr


class Steps:
    """
    Class Steps
    """

    def __init__(self, data: dict[str, ray.data.dataset.MaterializedDataset], enumerator: dict, archetype: dict):
        """

        :param data:
        :param enumerator:
        :param archetype:
        """

        self.__data = data
        self.__enumerator = enumerator
        self.__archetype = archetype

        self.__variable = vr.Variable(
            N_TRAIN=self.__data['train'].count(), N_VALID=self.__data['validate'].count(),
            N_TEST=self.__data['test'].count())

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self):
        """

        :return:
        """

        self.__logger.info(self.__data)
        self.__logger.info(self.__data['train'].take(1))
