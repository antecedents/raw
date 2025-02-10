"""Module interface.py"""
import logging

import boto3

import config
import src.elements.sources
import src.functions.directories
import src.s3.configurations
import src.source.data


class Interface:
    """
    Class Interface
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector: An instance of boto3.session.Session
        """

        self.__connector = connector

        # Hence
        self.__configurations = config.Config()



    def __sources(self):
        """
        Retrieves the uniform resource locator strings of the data, and its references.

        :return:
        """

        dictionary = src.s3.configurations.Configurations(connector=self.__connector).serial(
            key_name=self.__configurations.sources)

        return src.elements.sources.Sources(**dictionary)

    def exc(self):
        """

        :return:
        """

        # The uniform resource locator strings of the references & data
        sources = self.__sources()
        logging.info(sources)

        # GET
        src.source.data.Data(url=sources.data).exc()
