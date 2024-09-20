
import numpy as np

import transformers
import torch

import src.elements.variable as vr


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

        :param node:
        :return:
        """

        # A sentence's words, and the tokenization of words
        words: list[str] = node['sentence'].strip().split()
        encoding: dict = self.__tokenizer(words, padding='max_length', truncation=True,
                                          is_split_into_words=True,
                                          max_length=self.__variable.MAX_LENGTH,
                                          return_offsets_mapping=True)

        # placeholder array of labels for the encoding dict
        ela: np.ndarray = np.ones(shape=self.__variable.MAX_LENGTH, dtype=int) * -100

        # The corresponding tags of a sentence's words, and the code of each tag
        tags: list[str] = node['tagstr'].split(',')
        labels = [self.__enumerator[tag] for tag in tags]

        # Herein, per iteration, cf. offset pairings.  There
        # are <max_length> iterations/offset pairings.
        # (maximum number of tokens, 2)
        limit = len(labels)
        for iteration, mapping in enumerate(encoding['offset_mapping']):
            if mapping[0] == 0 and mapping[1] != 0 and iteration < limit:
                ela[iteration] = labels[iteration]

        # Hence, set.
        encoding['labels'] = ela

        # Beware of the steps herein: (a) as tensors, and (b) to graphics processing unit, i.e.,
        # CUDA (computer unified device architecture)
        item = {key: torch.as_tensor(value).cuda() for key, value in encoding.items()}

        return item
