"""Module interface.py"""
import logging
import typing

import pandas as pd
import datasets
import ray.data

import src.data.splittings


class Interface:
    """
    Interface: Data
    """

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__data = data

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger(__name__)

    def __splits(self) -> typing.Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

        training, validating, testing = src.data.splittings.Splittings(
            data=self.__data).exc()
        training.info()
        validating.info()
        testing.info()

        return training, validating, testing


    def get_datasets(self) -> datasets.DatasetDict:

        training, validating, testing = self.__splits()

        return datasets.DatasetDict({
            'train': datasets.Dataset.from_pandas(training),
            'validate': datasets.Dataset.from_pandas(validating),
            'test': datasets.Dataset.from_pandas(testing)
        })


    def get_rays(self) -> dict[str, ray.data.dataset.MaterializedDataset]:

        __datasets = self.get_datasets()

        return {
            'train': ray.data.from_huggingface(__datasets['train']),
            'validate': ray.data.from_huggingface(__datasets['validate']),
            'test': ray.data.from_huggingface(__datasets['test'])
        }
