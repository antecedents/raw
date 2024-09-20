
import logging

import src.models.bert.architecture
import src.elements.variable as vr

import ray.train.torch
import ray.train
import ray.tune
import ray.tune.schedulers


class Interface:

    def __init__(self, data: dict[str, ray.data.dataset.MaterializedDataset],
                 variable: vr.Variable, enumerator: dict):

        self.__data = data
        self.__variable = variable
        self.__enumerator = enumerator

        # Maximum steps per epoch
        self.__max_steps_per_epoch: int = (
                self.__variable.N_TRAIN // (self.__variable.TRAIN_BATCH_SIZE * self.__variable.N_GPU))

    def exc(self):

        arc = src.models.bert.architecture.Architecture()

        # From Hugging Face Trainer -> Ray Trainer
        trainable = ray.train.torch.TorchTrainer(
            arc.exc,
            datasets={'train': self.__data['train'], 'eval': self.__data['validate']}
        )

        tuner = ray.tune.Tuner(
            trainable,
            param_space={
                'train_loop_config': {
                    'learning_rate': ray.tune.grid_search([0.01, 0.02]),
                    'weight_decay': ray.tune.grid_search([0.1, 0.2]),
                    'max_steps_per_epoch': self.__max_steps_per_epoch,
                    'variable': self.__variable,
                    'enumerator': self.__enumerator
                },
                'scaling_config': ray.train.ScalingConfig(
                    num_workers=self.__variable.N_GPU, use_gpu=True, trainer_resources={'CPU': self.__variable.N_CPU})
            }

        )
