"""Module steps.py"""
import logging

import ray.data.dataset
import ray.tune
import ray.air

import src.elements.variable as vr
import src.models.bert.interface
import src.models.bert.valuation


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
            N_TEST=self.__data['test'].count(), EPOCHS=2)

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

        example = self.__data['train'].take(1)
        self.__logger.info(example[0])
        self.__logger.info(example[0]['sentence'])
        self.__logger.info(type(example))

        results: ray.tune.ResultGrid = src.models.bert.interface.Interface(
            data=self.__data, variable=self.__variable,
            enumerator=self.__enumerator, archetype=self.__archetype).exc()

        best: ray.air.Result = results.get_best_result()
        src.models.bert.valuation.Valuation().exc(best=best)
