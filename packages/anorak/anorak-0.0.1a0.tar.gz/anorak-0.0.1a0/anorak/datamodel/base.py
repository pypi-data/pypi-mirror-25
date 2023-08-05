import typing
from anorak.dataset import DataSet

class DataModel(object):

    """
    A DataModel contains a list of data sets and associated meta data describing
    the relationships between individual data sets in the list. Anonymizers that
    return more than one data set as a result can use a `DataModel` instance to
    to describe the relationships between the individual data sets they return.
    This is e.g. useful when dealing with databases that contain multiple tables
    which are related to each other via foreign keys, or when generating
    anonymized data that is spread out over multiple data sets (such as the
    results produced by the `Anatomy` anomyizer).
    """

    def __init__(self,
                 datasets : typing.Dict[str, DataSet],
                 metadata : typing.Dict[str, typing.Any]):
        """
        :param datasets: A list of `DataSet` instances.
        :param metadata: A meta data object describing the relationships of the
                         data sets.
        """
        self.datasets = datasets
        self.metadata = metadata