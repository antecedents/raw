"""config.py"""
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
