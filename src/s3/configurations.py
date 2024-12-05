import logging

import boto3

import yaml
import src.functions.secret
import src.s3.unload


class Configurations:

    def __init__(self, connector: boto3.session.Session):

        self.__s3_client: boto3.session.Session.client = connector.client(
            service_name='s3')

        self.__secret = src.functions.secret.Secret(connector=connector)

    def __get_dictionary(self, key_name: str) -> dict:
        """

        :return:
            A dictionary of YAML file contents
        """

        buffer = src.s3.unload.Unload(s3_client=self.__s3_client).exc(
            bucket_name=self.__secret.exc(secret_id='NumericIntelligence', node='c_emergency'),
            key_name=key_name)

        try:
            data: dict = yaml.load(stream=buffer, Loader=yaml.CLoader)
        except yaml.YAMLError as err:
            raise err from err

        logging.info(data['parameters'])

        return data['parameters']

    def __call__(self, key_name: str):

        return self.__get_dictionary(key_name=key_name)
