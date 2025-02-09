import pandas as pd
import numpy as np

class Inspect:

    def __init__(self, data: pd.DataFrame):

        self.__data = data

    def __department_type(self):

        tensor: np.ndarray = self.__data['DepartmentType'].unique()

        assert tensor.shape[0] == 1, 'The # of distinct department types is > 1'
        assert np.all(np.char.equal(tensor, 'Type 1')), 'The department type of each instance must be Type 1'

    def __country(self):

        country_code = 'S92000003'

        tensor = self.__data['Country'].unique()

        assert tensor.shape[0] == 1, f'Error.  The data should be the data of a single country; {tensor.shape[0]} countries are present.'
        assert np.all(np.char.equal(tensor, country_code)), f'Invalid country code.  The country code of each instance should be {country_code}'


