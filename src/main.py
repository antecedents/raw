"""Module main.py"""
import logging
import os
import sys

import pandas as pd
import torch


def main():
    """

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)

    # Device  Selection: Setting a graphics processing unit as the default device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(msg=device)

    # The raw data
    data = src.data.source.Source().exc()
    elements = src.data.tags.Tags(data=data).exc()
    enumerator, archetype = src.data.encodings.Encodings().exc(elements=elements)

    # Hence, the expected structure.  Within the preceding dataframe each distinct sentence
    # is split across rows; a word per row, in order.  The Specimen class re-constructs the
    # original sentences.
    data: pd.DataFrame = data.copy().loc[data['category'].isin(values=elements['category'].unique()), :]
    specimens: pd.DataFrame = src.data.specimens.Specimens(data=data, elements=elements).exc()

    # Modelling
    src.models.interface.Interface(specimens=specimens).exc()


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Classes
    import src.data.encodings
    import src.models.interface
    import src.data.source
    import src.data.specimens
    import src.data.tags

    main()
