
import logging

import src.models.bert.architecture

import ray.train.torch


class Interface:

    def __init__(self, data: dict[str, ray.data.dataset.MaterializedDataset]):

        self.__data = data
        logging.info(self.__data['train'].count())

    def exc(self):

        arc = src.models.bert.architecture.Architecture()

        # From Hugging Face Trainer -> Ray Trainer
        trainable = ray.train.torch.TorchTrainer(
            arc.exc,
            datasets={"train": self.__data["train"], "eval": self.__data["validate"]}
        )

