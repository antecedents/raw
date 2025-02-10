"""Module arguments.py"""
import argparse

class Arguments:
    """
    Notes<br>
    ------<br>

    Processes the project's input arguments.
    """

    def __init__(self):
        pass

    @staticmethod
    def restart(value):
        """

        :param value:
        :return:
        """

        if str(value) != 'restart':
            raise argparse.ArgumentTypeError('The only valid value of this optional argument is restart')

        return True
