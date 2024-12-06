import logging

import boto3

import yaml
import json
import src.functions.secret
import src.s3.unload


class Configurations:

    def __init__(self, connector: boto3.session.Session):

        self.__s3_client: boto3.session.Session.client = connector.client(
            service_name='s3')

        self.__secret = src.functions.secret.Secret(connector=connector)

    def __buffer(self, key_name: str):

        buffer = src.s3.unload.Unload(s3_client=self.__s3_client).exc(
            bucket_name=self.__secret.exc(secret_id='NumericIntelligence', node='c_emergency'),
            key_name=key_name)

        return buffer

    def serial(self, key_name: str) -> dict:
        """

        :return:
            A dictionary of YAML file contents
        """

        try:
            data: dict = yaml.load(stream=self.__buffer(key_name=key_name), Loader=yaml.CLoader)
        except yaml.YAMLError as err:
            raise err from err

        logging.info(data['parameters'])

        return data['parameters']

    def objects(self, key_name: str):

        try:
            data = json.loads(self.__buffer(key_name=key_name))
        except json.JSONDecodeError as err:
            raise err from err

        logging.info(data)

        return data
