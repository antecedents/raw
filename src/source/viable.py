import pandas as pd


class Viable:

    def __init__(self, arguments: dict):

        self.__arguments = arguments

    def __filter(self, blob: pd.DataFrame):
        """

        :param blob:
        :return:
        """

        # Counts per institution
        counts: pd.DataFrame = blob.copy()[['health_board_code', 'hospital_code']].groupby(
            by='health_board_code').value_counts().to_frame()
        counts.reset_index(inplace=True)

        # Institutions that have a viable number of observations.
        viable: pd.DataFrame = counts.loc[counts['count'] >= (
                self.__arguments.get('seasons') * self.__arguments.get('cycles')), :]

        return viable

    def exc(self, data: pd.DataFrame):

        filter = self.__filter(blob=data)
