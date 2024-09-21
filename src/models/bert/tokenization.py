import typing
import numpy as np

import transformers
import torch

import src.elements.variable as vr
import src.models.bert.dataset


class Tokenization:

    def __init__(self, variable: vr.Variable, enumerator: dict,
                 tokenizer: transformers.tokenization_utils_base):
        """

        :param variable:
        :param enumerator:
        :param tokenizer:
        """

        self.__variable = variable
        self.__enumerator = enumerator
        self.__tokenizer = tokenizer

    # noinspection DuplicatedCode
    def exc(self, node: dict):
        """
        Under development

        :param node:
        :return:
        """

        '''
        Example
        -------
        
        https://docs.ray.io/en/latest/data/api/doc/ray.data.Dataset.iter_torch_batches.html
        
        node = {
            'sentence_identifier': np.array(['Sentence: 29552', 'Sentence: 28377', 'Sentence: 41530', 'Sentence: 15254']),
            'sentence': np.array([
                'Reigning overall champion Bode Miller of the United States finished 11th , nearly 2.5 seconds behind Rahlves .',
                'A U.S. military spokeswoman in Kabul says it is up to the Afghan government how it wants to deal with the broadcasts .',
                'She said he was being investigated for possible links to the al-Qaida terrorist network .',
                "Togo 's new President Faure Gnassingbe has visited his counterpart in Gabon , amid intense international pressure on the Togolese leader to step down ."
            ]),
            'tagstr': np.array([
                'O,O,O,B-per,I-per,O,O,B-geo,I-geo,O,B-tim,O,O,O,O,O,B-per,O',
                'O,B-geo,O,O,O,B-geo,O,O,O,O,O,O,B-gpe,O,O,O,O,O,O,O,O,O,O',
                'O,O,O,O,O,O,O,O,O,O,O,B-org,O,O,O',
                'B-geo,O,O,B-per,I-per,I-per,O,O,O,O,O,B-geo,O,O,O,O,O,O,O,O,O,O,O,O,O'])}
        '''

        T = typing.TypeVar('T', str, bytes)
        matrix: np.ndarray[T] = np.stack((node['sentence'], node['tagstr']), axis=-1, dtype=...)

        return src.models.bert.dataset.Dataset(
            matrix=matrix, variable=self.__variable, enumerator=self.__enumerator, tokenizer=self.__tokenizer)
