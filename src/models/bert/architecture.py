import logging

import ray.train
import transformers

import src.models.bert.tokenizer
import src.models.bert.special
import src.elements.variable as vr
import src.models.bert.parameters


class Architecture:

    def __init__(self):
        pass

    @staticmethod
    def exc(config: dict):

        logging.info(config)

        # Via config
        variable: vr.Variable = config.get('variable')
        max_steps_per_epoch: int = (
                variable.N_TRAIN // (variable.TRAIN_BATCH_SIZE * variable.N_GPU))

        # Parameters
        parameters = src.models.bert.parameters.Parameters()

        # Tokenizer
        tokenizer = src.models.bert.tokenizer.Tokenizer().exc()

        # Special
        special = src.models.bert.special.Special(
            variable=config.get('variable'), enumerator=config.get('enumerator'), tokenizer=tokenizer)

        training = ray.train.get_dataset_shard('train')
        evaluating = ray.train.get_dataset_shard('eval')

        training_ = training.iter_torch_batches(
            batch_size=variable.TRAIN_BATCH_SIZE, collate_fn=special.exc)
        evaluating_ = evaluating.iter_torch_batches(
            batch_size=variable.VALID_BATCH_SIZE, collate_fn=special.exc)

        # Arguments
        transformers.TrainingArguments(
            output_dir=parameters.MODEL_OUTPUT_DIRECTORY,
            eval_strategy='epoch', save_strategy='epoch',
            learning_rate=config.get('learning_rate'),
            weight_decay=config.get('weight_decay'),
            per_device_train_batch_size=variable.TRAIN_BATCH_SIZE,
            per_device_eval_batch_size=variable.VALID_BATCH_SIZE,
            num_train_epochs=variable.EPOCHS,
            max_steps=max_steps_per_epoch * variable.EPOCHS,
            warmup_steps=0,
            no_cuda=False
        )
