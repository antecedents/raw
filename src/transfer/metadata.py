import os
import logging
import boto3

import src.functions.objects
import src.s3.configurations


class Metadata:

    def __init__(self, connector: boto3.session.Session):

        self.__connector = connector

        self.__objects = src.functions.objects.Objects()

    def exc(self) -> dict:

        # uri = os.path.join(os.getcwd(), 'data', 'metadata.json')
        # dictionary = self.__objects.read(uri=uri)

        dictionary = src.s3.configurations.Configurations(connector=self.__connector).objects(
            key_name='raw/metadata.json')
        logging.info(dictionary)

        return dictionary
