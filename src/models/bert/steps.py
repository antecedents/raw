"""Module steps.py"""
import logging

import ray.data.dataset

import src.elements.frames as fr
import src.elements.variable as vr
import src.models.bert.tokenizer
import src.data.datatypes


class Steps:
    """
    Class Steps
    """

    def __init__(self, splittings: fr.Frames, enumerator: dict, archetype: dict):
        """

        :param splittings:
        :param enumerator:
        :param archetype:
        """

        self.__splittings = splittings
        self.__enumerator = enumerator
        self.__archetype = archetype

        self.__variable = vr.Variable(
            N_TRAIN=self.__splittings.training.shape[0], N_VALID=self.__splittings.validating.shape[0],
            N_TEST=self.__splittings.testing.shape[0])

        self.__tokenizer = src.models.bert.tokenizer.Tokenizer().exc()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self):
        """

        :return:
        """

        data: dict[str, ray.data.dataset.MaterializedDataset] = src.data.datatypes.Datatypes(
            splittings=self.__splittings).get_rays()

        self.__logger.info(type(data))
        self.__logger.info(data)
