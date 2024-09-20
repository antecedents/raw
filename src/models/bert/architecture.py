import logging

import ray.train

import src.models.bert.tokenizer
import src.models.bert.special


class Architecture:

    def __init__(self):
        pass

    @staticmethod
    def exc(config: dict):

        logging.info(config)

        # Tokenizer
        tokenizer = src.models.bert.tokenizer.Tokenizer().exc()

        # Special
        special = src.models.bert.special.Special(
            variable=config.get('variable'), enumerator=config.get('enumerator'), tokenizer=tokenizer)

        # Data & Tokens
        training = ray.train.get_dataset_shard('train')
        evaluating = ray.train.get_dataset_shard('eval')

        training_ = training.iter_torch_batches(
            batch_size=config.get('train_batch_size'), collate_fn=special.exc)
        evaluating_ = evaluating.iter_torch_batches(
            batch_size=config.get('valid_batch_size'), collate_fn=special.exc)
