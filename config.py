"""config.py"""
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        ------------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>
        """

        # Temporary local storage
        self.data_ = os.path.join(os.getcwd(), 'warehouse', 'data')
        self.raw_ = os.path.join(self.data_, 'raw')
        self.modelling_ = os.path.join(self.data_, 'modelling')

        # Configurations files, paths
        self.s3_parameters_key = 's3_parameters.yaml'
        self.sources = 'sources.yaml'
        self.metadata_ = 'metadata'
