"""Module main.py"""
import logging
import os
import sys

import ray
import torch


def main():
    """

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)

    # Device  Selection: Setting a graphics processing unit as the default device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(msg=device)

    # Ray
    ray.init(dashboard_host='172.17.0.2', dashboard_port=8265)

    # The raw data
    data = src.data.source.Source().exc()
    elements = src.data.tags.Tags(data=data).exc()
    enumerator, archetype = src.data.encodings.Encodings().exc(elements=elements)

    # Filtering
    filtering = src.data.filtering.Filtering()
    data = filtering(data=data, elements=elements)

    # Structuring
    data = src.data.structuring.Structuring(data=data).exc()

    # Modelling
    src.models.interface.Interface(
        data=data, enumerator=enumerator, archetype=archetype).exc(architecture='bert')


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Activate graphics processing units
    os.environ['CUDA_VISIBLE_DEVICES']='0'
    os.environ['TOKENIZERS_PARALLELISM']='true'
    os.environ['RAY_USAGE_STATS_ENABLED']='0'

    # Classes
    import src.data.encodings
    import src.models.interface
    import src.data.source
    import src.data.filtering
    import src.data.structuring
    import src.data.tags

    main()
