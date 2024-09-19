import logging

import ray.train


class Architecture:

    def __init__(self):
        pass

    @staticmethod
    def exc(config: dict):

        logging.info(config)

        # Data & Tokens
        training = ray.train.get_dataset_shard("train")
        evaluating = ray.train.get_dataset_shard("eval")
