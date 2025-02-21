"""Module arguments.py"""
import argparse
import ast

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

        if isinstance(ast.literal_eval(value), bool):
            return ast.literal_eval(value)

        raise argparse.ArgumentTypeError('The only valid value of this optional argument is restart')
