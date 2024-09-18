"""Module tags.py"""
import logging

import pandas as pd

import config


class Tags:
    """
    Tags
    ----

    Description
    -----------
    This class determines the viable tags via category
    frequency; tag ≡ annotation ⧺ category

    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        A data frame that includes the tag, annotation, and category
        fields; remember, tag ≡ annotation ⧺ category

        :param data: The modelling data
        """

        self.__data = data

        # Tag fields
        self.__tag_fields: list[str] = ['tag', 'annotation', 'category']

        # Categories
        self.__mcf: int = config.Config().minimum_category_frequency

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger: logging.Logger = logging.getLogger(name=__name__)

    def __tag_data(self):
        """

        :return:
        """

        frame = self.__data.copy()[self.__tag_fields]

        # Frequencies
        elements: pd.DataFrame = frame.groupby(by=self.__tag_fields).value_counts().to_frame()
        elements.reset_index(drop=False, inplace=True)

        return elements

    def __applicable(self, blob: pd.DataFrame) -> pd.DataFrame:
        """
        
        :param blob: A frame that includes {category}, and {count} per category
        """

        categories: pd.DataFrame = blob[['category', 'count']].groupby(by='category').sum().reset_index(drop=False)
        categories = categories.copy().loc[categories['count'] >= self.__mcf, :]

        elements: pd.DataFrame = blob.copy().loc[
            blob['category'].isin(values=categories['category'].values), :]
        elements.sort_values(by='tag', inplace=True)

        return elements

    def exc(self) -> pd.DataFrame:
        """

        :return:
            pd.DataFrame: tag | annotation | category
        """

        # The tag data, including the count per distinct tag
        elements = self.__tag_data()

        # Focusing on viable/applicable categories
        elements = self.__applicable(blob=elements)

        return elements
