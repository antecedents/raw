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

        self.datapath = os.path.join(os.getcwd(), 'data')
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')

        # Addressing category imbalance ...
        self.minimum_category_frequency = 1000

        # Seed: All cases
        self.seed = 5
