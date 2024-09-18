"""Module interface.py"""
import logging


class Interface:
    """
    Interface: Models
    """

    def __init__(self):
        """

        :param specimens:
        """

        # Logging
        logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)


    def exc(self):
        """

        :return:
        """

        pass
