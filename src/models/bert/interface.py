
import logging

import src.models.bert.architecture
import src.elements.variable as vr

import ray.train.torch
import ray.tune
import ray.tune.schedulers


class Interface:

    def __init__(self, data: dict[str, ray.data.dataset.MaterializedDataset],
                 variable: vr.Variable, enumerator: dict):

        self.__data = data
        logging.info(self.__data['train'].count())

    def exc(self):

        arc = src.models.bert.architecture.Architecture()

        # From Hugging Face Trainer -> Ray Trainer
        trainable = ray.train.torch.TorchTrainer(
            arc.exc,
            datasets={"train": self.__data["train"], "eval": self.__data["validate"]}
        )

        tuner = ray.tune.Tuner(
            trainable,
            param_space={

            }

        )





