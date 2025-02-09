"""Module inspect.py"""
import numpy as np
import pandas as pd


class Inspect:

    def __init__(self, data: pd.DataFrame):
        """

        :param data:
        """

        self.__data = data

    def __department_type(self):
        """

        :return:
        """

        tensor: np.ndarray = self.__data['DepartmentType'].unique()

        assert tensor.shape[0] == 1, 'The # of distinct department types is > 1'
        assert np.all(np.char.equal(tensor, 'Type 1')), 'The department type of each instance must be Type 1'

    def __country(self):
        """

        :return:
        """

        c_country = 'S92000003'

        tensor = self.__data['Country'].unique()

        assert tensor.shape[0] == 1, \
            f'Error.  The data should be the data of a single country; {tensor.shape[0]} countries are present.'
        assert np.all(np.char.equal(tensor, c_country)), \
            f'Invalid country code.  The country code of each instance should be {c_country}'

    def __attendance_category(self):
        """

        :return:
        """

        c_attendance_category = 'Unplanned'

        tensor: np.ndarray = self.__data['AttendanceCategory'].unique()

        assert tensor.shape[0] == 1, \
            'The # of attendance categories is > 1; there should be 1, i.e., Unplanned, only.'
        assert np.all(np.char.equal(tensor, c_attendance_category)), \
            f'Invalid attendance category.  The attendance category of each instance should be {c_attendance_category}'
