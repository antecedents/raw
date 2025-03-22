"""Module interface.py"""
import logging

import boto3

import config
import src.elements.sources
import src.functions.directories
import src.s3.configurations
import src.source.data
import src.source.dates
import src.source.viable


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

    def __get_dictionary(self, key_name: str):
        """
        Retrieves the uniform resource locator strings of the data, and its references.

        :return:
        """

        dictionary = src.s3.configurations.Configurations(connector=self.__connector).serial(
            key_name=key_name)['parameters']

        return dictionary

    def exc(self):
        """

        :return:
        """

        # The uniform resource locator strings of the references & data
        dictionary = self.__get_dictionary(key_name=self.__configurations.sources)
        sources = src.elements.sources.Sources(**dictionary)
        logging.info(sources)

        # The set of modelling & decomposition arguments, vis-à-vis forecasting algorithm and supplements.
        arguments = self.__get_dictionary(key_name=self.__configurations.attributes)
        logging.info(arguments)

        # GET
        data = src.source.data.Data(url=sources.data).exc()

        # Focus
        data = data.copy()[self.__configurations.fields]

        # Address dates, and anomalies thereof
        data = src.source.dates.Dates(data=data).exc()

        # Viability: Focusing on institutions that have sufficient instances for modelling, etc.
        src.source.viable.Viable(arguments=arguments).exc(data=data)
