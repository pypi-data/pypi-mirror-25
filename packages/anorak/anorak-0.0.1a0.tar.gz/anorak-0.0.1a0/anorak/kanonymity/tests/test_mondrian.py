import unittest
from .data import data
from anorak.kanonymity import Mondrian

class MondrianTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_k_anonymity(self):
        config = {
            'k' : 5
        }
        anonymizer = Mondrian(**config)

        result = anonymizer.anonymize(data['adult'])

        assert len(result) == 18
