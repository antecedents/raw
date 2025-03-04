"""Module main.py"""
import argparse
import datetime
import logging
import os
import sys

import boto3


def main():
    """
    Entry point.

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('Starting: %s', datetime.datetime.now().isoformat(timespec='microseconds'))

    # Set up
    setup: bool = src.setup.Setup(service=service, s3_parameters=s3_parameters, restart=restart).exc()
    if not setup:
        src.functions.cache.Cache().exc()
        sys.exit('No Executions')

    # Hence
    src.source.interface.Interface(connector=connector).exc()
    src.transfer.interface.Interface(
       connector=connector, service=service, s3_parameters=s3_parameters).exc()

    # Cache
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Classes
    import src.functions.arguments
    import src.functions.cache
    import src.functions.service
    import src.s3.s3_parameters
    import src.setup
    import src.source.interface
    import src.transfer.interface

    arguments = src.functions.arguments.Arguments()
    parser = argparse.ArgumentParser()
    parser.add_argument('--restart', type=arguments.restart,
                        help='The valid strings are True, which deletes raw data assets, or False, which leaves the assets alone.')
    args = parser.parse_args()

    # Restart
    restart = False if args.restart is None else args.restart

    # S3 S3Parameters, Service Instance
    connector = boto3.session.Session()
    s3_parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
    service = src.functions.service.Service(connector=connector, region_name=s3_parameters.region_name).exc()

    main()
