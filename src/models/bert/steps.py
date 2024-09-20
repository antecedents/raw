"""Module steps.py"""
import logging

import ray.data.dataset
import ray.tune

import src.elements.variable as vr
import src.models.bert.interface


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

        results: ray.tune.ResultGrid = src.models.bert.interface.Interface(
            data=self.__data, variable=self.__variable,
            enumerator=self.__enumerator, archetype=self.__archetype).exc()

        best = results.get_best_result()
        self.__logger.info(best.metrics_dataframe)
        self.__logger.info(best.checkpoint)
        self.__logger.info(best.best_checkpoints)
