"""Module dates.py"""
import logging

import dask
import pandas as pd


class Dates:
    """
    Notes<br>
    ------<br>

    Unfortunately, the delivery day of the week is uncertain.  Hence, this project will initially
    assume that the points of an institution's series are contiguous.  Do not use this class yet.
    """

    def __init__(self, frame: pd.DataFrame):
        """

        :param frame:
        """

        self.__frame = frame

    @dask.delayed
    def __indices(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        minimum: pd.Timestamp = blob['week_ending_date'].min()
        maximum: pd.Timestamp = blob['week_ending_date'].max()

        indices: pd.DataFrame = pd.date_range(start=minimum, end=maximum, inclusive='both', freq='W-SUN').to_frame()
        indices.reset_index(drop=True, inplace=True)
        indices.rename(columns={0: 'week_ending_date'}, inplace=True)
        logging.info(indices)

        return indices

    @dask.delayed
    def __get_data(self, code: str) -> pd.DataFrame:
        """

        :param code:
        :return:
        """

        return self.__frame.copy().loc[self.__frame['hospital_code'] == code, :]

    @dask.delayed
    def __dates(self, indices: pd.DataFrame, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param indices: Dates
        :param blob:
        :return:
        """

        # Common Values
        fields = ['health_board_code', 'hospital_code', 'department_type', 'attendance_category']
        reference = blob[fields].drop_duplicates().values

        # Ascertaining all date points within a range
        frame = indices.merge(blob, how='left', on='week_ending_date')
        frame.loc[:, fields] = reference

        return frame

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        codes = self.__frame['hospital_code'].unique()

        computations = []
        for code in codes:
            blob = self.__get_data(code=code)
            indices = self.__indices(blob=blob.copy())
            frame = self.__dates(indices=indices, blob=blob.copy())
            computations.append(frame)
        calculations = dask.compute(computations, scheduler='threads')[0]
        data = pd.concat(calculations, axis=0, ignore_index=True)
        data.to_csv(path_or_buf='test.csv', index=False, header=True, encoding='utf-8')
        logging.info(data)

        return data
