
import src.elements.frames as fa
import src.elements.variable as vr

import src.models.bert.dataset as dt
import src.models.bert.tokenizer


class Steps:

    def __init__(self, splittings: fa.Frames, enumerator: dict, archetype: dict):

        self.__splittings = splittings
        self.__enumerator = enumerator
        self.__archetype = archetype

        self.__variable = vr.Variable(
            N_TRAIN=self.__splittings.training.shape[0], N_VALID=self.__splittings.validating.shape[0],
            N_TEST=self.__splittings.testing.shape[0])

        self.__tokenizer = src.models.bert.tokenizer.Tokenizer()


    def exc(self):

        training = dt.Dataset(frame=self.__splittings.training, variable=self.__variable,
                              enumerator=self.__enumerator, tokenizer=self.__tokenizer)
        validating = dt.Dataset(frame=self.__splittings.validating, variable=self.__variable,
                                enumerator=self.__enumerator, tokenizer=self.__tokenizer)
        testing = dt.Dataset(frame=self.__splittings.testing, variable=self.__variable,
                             enumerator=self.__enumerator, tokenizer=self.__tokenizer)

        training
