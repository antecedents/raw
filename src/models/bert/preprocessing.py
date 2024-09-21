import transformers

import src.elements.variable as vr
import src.models.bert.parameters
import src.models.bert.parameters


class Preprocessing:

    def __init__(self, tokenizer: transformers.PreTrainedTokenizerFast, variable: vr.Variable):

        self.__tokenizer = tokenizer
        self.__variable = variable

        # Additionally
        self.__parameters = src.models.bert.parameters.Parameters()
