"""Module interface.py"""
import logging

import boto3

import config
import src.elements.sources
import src.functions.directories
import src.s3.configurations
import src.source.data
import src.source.viable
import src.source.dates


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
            key_name=self.__configurations.sources)['parameters']

        return src.elements.sources.Sources(**dictionary)

    def __arguments(self) -> dict:
        """

        :return:
        """

        return src.s3.configurations.Configurations(connector=self.__connector).objects(
            key_name=('settings' + '/' + 'arguments.json')
        )

    def exc(self):
        """

        :return:
        """

        # The uniform resource locator strings of the references & data
        sources = self.__sources()
        logging.info(sources)

        # The set of modelling & decomposition arguments, vis-à-vis forecasting algorithm and supplements.
        arguments = self.__arguments()

        # GET
        data = src.source.data.Data(url=sources.data).exc()
        data = src.source.dates.Dates(data=data).exc()
        src.source.viable.Viable(arguments=arguments).exc(data=data)
