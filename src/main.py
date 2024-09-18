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
    data = src.data.source.Source().exc()
    elements = src.data.tags.Tags(data=data).exc()
    enumerator, archetype = src.data.encodings.Encodings().exc(elements=elements)


    # Hence, the expected structure.  Within the preceding dataframe each distinct sentence
    # is split across rows; a word per row, in order.  The Specimen class re-constructs the
    # original sentences.
    specimens = src.data.specimens.Specimens(data=data, elements=elements).exc()


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Classes
    import src.data.source
    import src.data.tags
    import src.data.encodings
    import src.data.specimens

    main()
