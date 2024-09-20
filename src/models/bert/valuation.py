import logging
import os

import ray.air
import ray.train
import transformers


class Valuation:

    def __init__(self):

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def exc(self, best: ray.air.Result):
        """

        :param best:
        :return:
        """

        # Properties
        self.__logger.info(best.metrics_dataframe)
        self.__logger.info(best.checkpoint)
        self.__logger.info(best.best_checkpoints)

        # Explore
        checkpoint = best.checkpoint

        with checkpoint.as_directory() as directory:
            path = os.path.join(directory, 'checkpoint')
            model = transformers.BertForTokenClassification.from_pretrained(
                pretrained_model_name_or_path=path)

        self.__logger.info(dir(model))
