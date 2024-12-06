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
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.data_ = [os.path.join(self.warehouse, 'raw', 'references'),
                      os.path.join(self.warehouse, 'raw', 'data'),
                      os.path.join(self.warehouse, 'latest', 'references'),
                      os.path.join(self.warehouse, 'latest', 'data')]

        # Configuration files
        self.s3_parameters_key = 's3_parameters.yaml'
        self.locators = 'locators.yaml'
