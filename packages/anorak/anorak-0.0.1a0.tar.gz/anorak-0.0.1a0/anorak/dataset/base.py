class DataSet(object):

    def __init__(self, data, metadata):
        self.data = data
        self.parse_metadata(metadata)

    def parse_metadata(self, metadata):
        self.metadata = metadata

    def append(self):
        pass
