import argparse

class Arguments:

    def __init__(self):
        pass

    @staticmethod
    def restart(value):

        if not str(value) == 'restart':
            raise argparse.ArgumentTypeError('The only valid value of this optional argument is restart')

        return True
