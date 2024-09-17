"""Module main.py"""
import logging
import os
import sys

import torch


def main():
    """

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)

    # Device  Selection: Setting a graphics processing unit as the default device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(msg=device)

    # Hence
    src.data.interface.Interface().exc()


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Classes
    import src.data.interface

    main()
