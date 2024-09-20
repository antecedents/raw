import transformers

import src.models.bert.parameters

class Tokenizer:

    def __init__(self):

        self.__parameters = src.models.bert.parameters.Parameters()

    def exc(self) -> transformers.tokenization_utils_base:
        """
        # https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoTokenizer
        transformers.AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=self.__parameters.pretrained_model_name,
            use_fast=True)

        :return:
        """

        # Tokenizer
        return transformers.BertTokenizerFast.from_pretrained(
            pretrained_model_name_or_path=self.__parameters.pretrained_model_name,
            clean_up_tokenization_spaces=True)
