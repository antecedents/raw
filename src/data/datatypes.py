"""Module datatypes.py"""
import datasets
import ray.data

import src.elements.frames as fr


class Datatypes:
    """
    Class Datatypes

    Provides different formats of the data splits.
    """

    def __init__(self, splittings: fr.Frames):
        """

        :param splittings:
        """

        self.__splittings = splittings

    def get_datasets(self) -> datasets.DatasetDict:
        """
        The datasets.DatasetDict format of the data splits

        :return:
        """

        return datasets.DatasetDict({
            'train': datasets.Dataset.from_pandas(self.__splittings.training),
            'validate': datasets.Dataset.from_pandas(self.__splittings.validating),
            'test': datasets.Dataset.from_pandas(self.__splittings.testing)
        })

    def get_rays(self) -> dict[str, ray.data.dataset.MaterializedDataset]:
        """
        The ray data format of the huggingface.co Datasets in datasets.DatasetDict

        :return:
        """

        __datasets = self.get_datasets()

        return {
            'train': ray.data.from_huggingface(__datasets['train']),
            'validate': ray.data.from_huggingface(__datasets['validate']),
            'test': ray.data.from_huggingface(__datasets['test'])
        }
