import transformers

import src.models.bert.parameters


class Intelligence:

    def __init__(self, enumerator: dict, archetype: dict):
        """

        :param enumerator:
        :param archetype:
        """

        self.__enumerator = enumerator
        self.__archetype = archetype

        # The parameters and their arguments.
        self.__parameters = src.models.bert.parameters.Parameters()

    @staticmethod
    def collator(tokenizer: transformers.tokenization_utils_base):
        """
        https://huggingface.co/docs/transformers/main_classes/data_collator#transformers.DataCollatorForTokenClassification

        :param tokenizer:
        :return:
        """

        return transformers.DataCollatorForTokenClassification(tokenizer=tokenizer)

    def model(self):

        config = transformers.BertConfig.from_pretrained(
            pretrained_model_name_or_path=self.__parameters.pretrained_model_name,
            **{'num_labels': len(self.__enumerator),
               'id2label': self.__enumerator,
               'label2id': self.__archetype})

        return transformers.BertForTokenClassification.from_pretrained(
            pretrained_model_name_or_path=self.__parameters.pretrained_model_name,
            config=config)

