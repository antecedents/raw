"""Module preprocessing.py"""
import transformers
import ray.data

import numpy as np
import torch

import src.elements.variable as vr
import src.models.bert.parameters
import src.models.bert.parameters


class Preprocessing:

    def __init__(self, tokenizer: transformers.PreTrainedTokenizerFast, variable: vr.Variable):
        """

        :param tokenizer:
        :param variable:
        """

        self.__tokenizer = tokenizer
        self.__variable = variable

        # Additionally
        self.__parameters = src.models.bert.parameters.Parameters()

    def __tokenization(self, blob):
        """
        Example:
         blob = {'sentence_identifier': np.array([..., ...]),
                 'sentence': np.array([..., ...]),
                 'tagstr': np.array([
                    'O,O,O,B-per,I-per,O,O,B-geo,I-geo,O,B-tim,O,O,O,O,O,B-per,O',
                    'O,B-geo,O,O,O,B-geo,O,O,O,O,O,O,B-gpe,O,O,O,O,O,O,O,O,O,O'])
                }

        :return:
        """


    def iterables(self, part: ray.data.DataIterator, batch_size: int):
        """

        :param part:
        :param batch_size:
        :return:
        """

        return part.iter_torch_batches(
            batch_size=batch_size, collate_fn=self.__tokenization)
