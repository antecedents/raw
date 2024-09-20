"""Module interface.py"""
import logging

import pandas as pd

import ray.data

import src.data.splittings
import src.elements.frames as fr
import src.models.bert.steps
import src.data.datatypes


class Interface:
    """
    Interface: Models
    """

    def __init__(self, data: pd.DataFrame, enumerator: dict, archetype: dict):
        """

        :param data:
        :param enumerator:
        :param archetype:
        """

        self.__splittings: fr.Frames = src.data.splittings.Splittings(data=data).exc()
        self.__enumerator = enumerator
        self.__archetype = archetype

        # Logging
        logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)


    def exc(self, architecture: str):
        """

        :param architecture:
        :return:
        """

        data: dict[str, ray.data.dataset.MaterializedDataset] = src.data.datatypes.Datatypes(
            splittings=self.__splittings).get_rays()

        match architecture:
            case 'bert':
                src.models.bert.steps.Steps(
                    data=data, enumerator=self.__enumerator, archetype=self.__archetype).exc()
            case 'distil':
                self.__logger.info('...')
            case 'electra':
                self.__logger.info('...')
            case _:
                self.__logger.info('?')
