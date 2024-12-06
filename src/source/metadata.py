import os
import logging

import src.functions.objects


class Metadata:

    def __init__(self):

        self.__objects = src.functions.objects.Objects()

    def exc(self):

        uri = os.path.join(os.getcwd(), 'data', 'metadata.json')
        dictionary = self.__objects.read(uri=uri)
        logging.info(dictionary)
