"""Module parameters.py"""
import typing
import os
import torch

import config


class Parameters(typing.NamedTuple):
    """

    Attributes
    ----------
    task : str
        The type of task the model is being trained for

    pretrained_model_name : str
        The name of the pre-trained model that will be fine-tuned

    device : str
        The processing unit device type

    storage_path : str
        For ray.train.RunConfig

    MODEL_OUTPUT_DIRECTORY: str
        A directory for model outputs.  For transformers.TrainingArguments

    Notes
    -----
    [from_pretrained](https://huggingface.co/docs/transformers/main_classes/model#transformers.PreTrainedModel.from_pretrained)
    [PretrainedConfig](https://huggingface.co/docs/transformers/main_classes/configuration#transformers.PretrainedConfig)
    """

    task: str = 'ner'
    pretrained_model_name: str = 'google-bert/bert-base-uncased'
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    MODEL_OUTPUT_DIRECTORY: str = os.path.join(config.Config().warehouse, 'bert')
    storage_path: str = os.path.join(config.Config().warehouse, 'bert')
