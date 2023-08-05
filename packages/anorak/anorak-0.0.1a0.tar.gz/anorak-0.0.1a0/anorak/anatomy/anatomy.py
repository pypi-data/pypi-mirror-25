from anorak import Anonymizer
from anorak.datamodel import DataModel

from collections import defaultdict

class Anatomy(Anonymizer):
    
    """
    Uses the "Anatomy" [1] method to anonymize a dataset by splitting it up into
    multiple tables and linking the tables together.

    1: Xiao, Xiaokui, and Yufei Tao. "Anatomy: Simple and effective privacy
       preservation." Proceedings of the 32nd international conference on
       Very large data bases. VLDB Endowment, 2006.
    """

    def __init__(self, l=4):
        """
        :param l: The l-diversity value that should be enfored in the anonymized
                  data set.
        """
        self.l = l

    def anonymize(self, x):
        """
        Anonymizes a dataset x.

        Algorithm:

        * set QIT=[], ST=[], gcnt=0
        * hash the input data X by sensitive attribute
        * while there are at least `l` non-empty hash buckets:
          - gcnt+=1
          - QI_{gcnt}=[]
          - S=(set of `l` largest buckets)
          - for each bucket in `S`:
            - remove an arbitrary tuple `t` from the bucket and add it to
              QI_{gcnt}
        * for each non-empty bucket:
          - get the remaining element from the bucket
          - assign it to the first QI_j group that does not yet contain the
            value t[d+1] (A_s) of the tuple
        * for j=1 to gcnt:
          - for each tuple t in QI_j:
            - insert tuple (t[1], ..., t[d], j) into QIT
          - for each distinct A_s=v value in QI_j:
            - c_j(v)=number of tuples in QI_j with value t[d+1]=v
            - insert record (j, v, c_j(v)) into ST
        * return QT and ST

        :param X: An instance of a `DataSet` class.
        :returns: A tuple containing two `DataSet` objects corresponding to the

        """
        #we group X by its sensitive columns
        vs = x.distinct(x.sensitive_columns)
        x_by_vs = x.groupby(x.sensitive_columns)

        n_by_v = defaultdict(lambda: 0)

        if len(vs) < self.l:
            raise ValueError("Data is not diverse enough:"
                             "Only {} distinct values, but {} are required."\
                             .format(len(vs), self.l))

        qt = self.make_dataset()
        st = self.make_dataset()

        model = DataModel([], {})
        return model
