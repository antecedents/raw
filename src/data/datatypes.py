"""Module datatypes.py"""
import datasets
import ray.data

import src.elements.frames as fr


class Datatypes:

    def __init__(self, splittings: fr.Frames):
        """

        :param splittings:
        """

        self.__splittings = splittings

    def get_datasets(self) -> datasets.DatasetDict:

        return datasets.DatasetDict({
            'train': datasets.Dataset.from_pandas(self.__splittings.training),
            'validate': datasets.Dataset.from_pandas(self.__splittings.validating),
            'test': datasets.Dataset.from_pandas(self.__splittings.testing)
        })

    def get_rays(self) -> dict[str, ray.data.dataset.MaterializedDataset]:

        __datasets = self.get_datasets()

        return {
            'train': ray.data.from_huggingface(__datasets['train']),
            'validate': ray.data.from_huggingface(__datasets['validate']),
            'test': ray.data.from_huggingface(__datasets['test'])
        }
