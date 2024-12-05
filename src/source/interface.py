import logging

import boto3

import config
import src.elements.locators
import src.functions.directories
import src.functions.secret
import src.s3.configurations
import src.s3.unload
import src.source.data


class Interface:

    def __init__(self, connector: boto3.session.Session):

        self.__connector = connector

        # Hence
        self.__configurations = config.Config()
        self.__secret = src.functions.secret.Secret(connector=connector)

    def __storage(self):
        """
        Creates all the paths for the graphing data.

        :return:
        """

        directories = src.functions.directories.Directories()

        for value in self.__configurations.data_:
            directories.create(value)

    def __locators(self):

        dictionary = src.s3.configurations.Configurations(connector=self.__connector).__call__(
            key_name=self.__configurations.locators)

        return src.elements.locators.Locators(**dictionary)

    def exc(self):

        # Preparing the temporary local storage areas
        self.__storage()

        # The uniform resource locator strings of the references & data
        locators = self.__locators()

        # GET
        src.source.data.Data(url=locators.data).exc()
