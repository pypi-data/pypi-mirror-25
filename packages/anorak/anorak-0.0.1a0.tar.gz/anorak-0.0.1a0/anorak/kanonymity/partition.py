import numpy as numpy
import pandas as pd


class Partition(object):

    def __init__(self, data, k, data_widths):
        ''' low/ high: list of indices referring to the lowest/ highest member of every column, 
            index w.r.t the (unique) value_list of a column 
        '''
        print('\t Init new partition...')
        self.k = k
        self.member = data.records
        self.qi_length = data.qi_length()
        self.allow = [1] * self.qi_length
        self.value_lists = data.value_lists()
        partition_widths = data.column_widths()
        self.norm_widths = self.get_norm_widths(data_widths, partition_widths)
        self.column_names = data.column_names
        #print('\n partition.allow %s' % self.allow)
        #print('\n partition.high %s' % self.high())

    def __len__(self):
        """
        return number of records
        """
        return len(self.member)

    def info(self):
        pass

    def low(self):
        # return Series with indices of column-wise minima
        return self.member.idxmin()

    def high(self):
        # return Series with indices of column-wise maxima
        return self.member.idxmax()

    def norm_width(self, data_width, part_width):
        """
        return Normalized width/ range of partition
        similar to NCP
        dim: column index, not name
        data_width: describes the width/ range of the data's column indexed by dim
        """
        try:
            norm_width = part_width * 1.0 / data_width
            #print('\n Norm_WIDTH: %s' % norm_width)
            return norm_width
        except ZeroDivisionError:
            return -1

    def get_norm_widths(self, data_widths, partition_widths):
        """
        return Normalized width/ range of partition
        similar to NCP
        column_widths: describes the widths/ range of the whole data's columns
        """
        norm_widths = []
        for dim in range(self.qi_length):
            data_col_width = data_widths[dim]
            part_col_width = partition_widths[dim]
            norm_widths.append( self.norm_width(data_col_width, part_col_width) )
        return norm_widths

    def choose_dimension(self):
        """
        chooss dim with largest norm_width from all attributes.
        This function can be upgraded with other distance function.
        """
        print('\t Choose dimension')
        max_width = -1
        max_dim = -1
        for dim in range(self.qi_length):
            if self.allow[dim] == 0:
                continue
            norm_width = self.norm_widths[dim]
            #print('\n MAXWIDTH: %s \t MAXDIM: %s \t WIDTH: %s \t DIM: %s' %(max_width, max_dim, norm_width, dim))
            if norm_width > max_width:
                max_width = norm_width
                max_dim = dim
        print('\t DIM: %s' % max_dim)
        return max_dim

    def find_median(self, dim):
        """
        find the middle of the partition, return splitVal
        """
        print('\t Compute median..')
        total = len(self.member.index)
        middle = total / 2
        value_list = self.value_lists[dim]
        if middle < self.k or len(value_list) <= 1:
            return None
        col_name = self.column_names[dim]
        col = self.member[col_name]
        median = col.quantile(interpolation='nearest')
        print('\t Median: %s' % median)
        return median

    def split_frame(self, value, dim):
        '''
        splits data frame in two frames lhs and rhs with lhs containing all values <= value
        '''
        print('\t Split frame.')
        col = self.column_names[dim]
        column = self.member[col]
        lhs = self.member[ column <= value ]
        rhs = self.member[ column > value ]
        return lhs, rhs


