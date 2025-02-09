import pandas as pd
import numpy as np

class Inspect:

    def __init__(self, data: pd.DataFrame):

        self.__data = data

    def __department_type(self):

        tensor: np.ndarray = self.__data['DepartmentType'].unique()

        assert tensor.shape[0] == 1, 'The # of distinct department types is > 1'
        assert np.all(np.char.equal(tensor, 'Type 1')), 'The department type of each instance must be Type 1'


