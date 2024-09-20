"""Module architecture.py"""
import logging
import os

import ray.train
import ray.train.huggingface.transformers as rt
import transformers

import src.elements.variable as vr
import src.models.bert.intelligence
import src.models.bert.metrics
import src.models.bert.parameters
import src.models.bert.tokenization
import src.models.bert.tokenizer


class Architecture:
    """
    Class Architecture
    """

    def __init__(self):
        pass

    @staticmethod
    def exc(config: dict):
        """
        
        :param config: 
        :return: 
        """

        logging.info(config)

        # Via config
        variable: vr.Variable = config.get('variable')
        max_steps_per_epoch: int = (
                variable.N_TRAIN // (variable.TRAIN_BATCH_SIZE * variable.N_GPU))

        # The parameters and their arguments.
        parameters = src.models.bert.parameters.Parameters()

        # Tokenizer
        tokenizer: transformers.tokenization_utils_base = src.models.bert.tokenizer.Tokenizer().exc()

        # Tokenization
        tke = src.models.bert.tokenization.Tokenization(
            variable=config.get('variable'), enumerator=config.get('enumerator'), tokenizer=tokenizer)

        training = ray.train.get_dataset_shard('train')
        evaluating = ray.train.get_dataset_shard('eval')

        training_ = training.iter_torch_batches(
            batch_size=variable.TRAIN_BATCH_SIZE, collate_fn=tke.exc)
        evaluating_ = evaluating.iter_torch_batches(
            batch_size=variable.VALID_BATCH_SIZE, collate_fn=tke.exc)

        # And
        metrics = src.models.bert.metrics.Metrics(
            archetype=config.get('archetype'))
        intelligence = src.models.bert.intelligence.Intelligence(
            enumerator=config.get('enumerator'), archetype=config.get('archetype'))

        # Arguments
        args = transformers.TrainingArguments(
            output_dir=parameters.MODEL_OUTPUT_DIRECTORY,
            eval_strategy='epoch', save_strategy='epoch',
            learning_rate=config.get('learning_rate'),
            weight_decay=config.get('weight_decay'),
            per_device_train_batch_size=variable.TRAIN_BATCH_SIZE,
            per_device_eval_batch_size=variable.VALID_BATCH_SIZE,
            num_train_epochs=variable.EPOCHS,
            max_steps=max_steps_per_epoch * variable.EPOCHS,
            warmup_steps=0,
            no_cuda=False,
            seed=config.get('seed'),
            save_total_limit=5,
            skip_memory_metrics=True,
            load_best_model_at_end=True,
            logging_dir=os.path.join(parameters.MODEL_OUTPUT_DIRECTORY, 'logs'),
            fp16=True,
            push_to_hub=False
        )

        # Trainer
        trainer = transformers.Trainer(
            model_init=intelligence.model,
            args=args,
            data_collator=intelligence.collator(tokenizer=tokenizer),
            train_dataset=training_,
            eval_dataset=evaluating_,
            tokenizer=tokenizer,
            compute_metrics=metrics.exc
        )
        trainer.add_callback(rt.RayTrainReportCallback())
        trainer = rt.prepare_trainer(trainer)

        trainer.train()
