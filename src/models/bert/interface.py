"""Module interface.py: The bert interface."""
import logging

import ray.train
import ray.train.torch
import ray.tune
import ray.tune.schedulers

import config
import src.elements.variable as vr
import src.models.bert.architecture
import src.models.bert.parameters
import src.models.bert.settings


class Interface:

    def __init__(self, data: dict[str, ray.data.dataset.MaterializedDataset],
                 variable: vr.Variable, enumerator: dict):
        """

        :param data:
        :param variable:
        :param enumerator:
        """

        self.__data = data
        self.__variable = variable
        self.__enumerator = enumerator

        # Parameters, and their arguments.
        self.__parameters = src.models.bert.parameters.Parameters()

        # Additionally
        self.__settings = src.models.bert.settings.Settings(variable=self.__variable)

    def exc(self):
        """

        :return:
        """

        arc = src.models.bert.architecture.Architecture()

        # From Hugging Face Trainer -> Ray Trainer
        trainable = ray.train.torch.TorchTrainer(
            arc.exc,
            datasets={'train': self.__data['train'], 'eval': self.__data['validate']}
        )

        # Tuner
        tuner = ray.tune.Tuner(
            trainable,
            param_space={
                'train_loop_config': {
                    'learning_rate': ray.tune.grid_search([0.01, 0.02]),
                    'weight_decay': ray.tune.grid_search([0.1, 0.2]),
                    'variable': self.__variable,
                    'enumerator': self.__enumerator,
                    'seed': config.Config().seed
                },
                'scaling_config': ray.train.ScalingConfig(
                    num_workers=self.__variable.N_GPU, use_gpu=True, trainer_resources={'CPU': self.__variable.N_CPU})
            },
            tune_config=ray.tune.TuneConfig(
                metric='eval_loss', mode='min',
                scheduler=self.__settings.scheduler(),
                num_samples=2, reuse_actors=True
            ),
            run_config=ray.train.RunConfig(
                name=self.__parameters.task,
                storage_path=self.__parameters.storage_path,
                progress_reporter=self.__settings.reporting(),
                checkpoint_config=ray.train.CheckpointConfig(
                    num_to_keep=5,
                    checkpoint_score_attribute='eval_loss',
                    checkpoint_score_order='min'
                )
            )

        )

        return tuner.fit()
