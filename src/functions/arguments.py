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
    def restart(value) -> bool:
        """

        :param value:
        :return:
        """

        if isinstance(eval(value), bool):
            return eval(value)
        else:
            raise argparse.ArgumentTypeError('The only valid value of this optional argument is restart')
