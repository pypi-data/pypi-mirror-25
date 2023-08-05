import numpy as numpy
import pandas as pd
import time
import os.path
from itertools import chain
import matplotlib

matplotlib.use('agg')

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Rectangle

from .partition import Partition

from anorak import Anonymizer

class Mondrian(Anonymizer):

    def __init__(self, k=10):
        self.k = k

    def anyonmize_partition(self, partition):
        print('Run anonymize..')
        #print('\n Partition: \n %s' %partition.member)
        allow_count = sum(partition.allow)
        print('\n ALLOW COUNT: %s ' %allow_count)
        if allow_count == 0:
            self.result.append(partition)
            print('\t ADD RESULT')
            return
        for index in range(allow_count):
            dim = partition.choose_dimension()
            if dim == -1:
                print("\t\t\t Error: dim=-1")
            median = partition.find_median(dim)
            lhs_frame, rhs_frame = partition.split_frame(median, dim)
            print('\t Check k-anonymity:')
            if ( rhs_frame.empty or len(lhs_frame.index) < self.k
                 or len(rhs_frame.index) < self.k ):
                print('\t Not valid, find new dim.')
                partition.allow[dim] = 0
                continue
            print('\t Valid, go on, init new lhs/ rhs Data')
            # find low/ high for new partitions lhs, rhs
            lhs_data = DataApp.Data(from_records=True, frame=lhs_frame)
            rhs_data = DataApp.Data(from_records=True, frame=rhs_frame)
            print('\t Init new partitions lhs, rhs')
            lhs = Partition(lhs_data, self.k, self.data_widths)
            rhs = Partition(rhs_data, self.k, self.data_widths)
            print('\t Anonymize lhs.')
            self.anonymize(lhs)
            print('\t Anonymize rhs.')
            self.anonymize(rhs)
            return
        self.result.append(partition)
        print('\t ADD RESULT')

    def anonymize(self, data, result=None):

        data_widths = self.get_column_widths(data)

        root_partition = Partition(data, self.k, data_widths)

        partitions = anonymize_partition(root_partition)

        if result is None:
            result = NumpyDataSet()

        result.meta['partitions'] = partitions

        for partition in partitions:
            result.append(...)

        return result

    def group_to_partition(self, partition):
        ''' for a single partition, extract and return intervals of (min,max)-values for each qi_column
            as well as a list of the indices of the initial dataframe's rows belonging to partition'''
        part_groups = partition.member.groupby(partition.column_names[:-1].tolist())
        group_specifier = list(part_groups.groups.keys())
        group_index_objects = list(part_groups.groups.values())
        group_indices_list = list(map(lambda x: list(x.values), group_index_objects))
        group_indices = list(chain.from_iterable(group_indices_list))
        group_values_list = list(zip(*group_specifier))
        group_intervals = [ (min(t), max(t)) for t in group_values_list ]
        return group_intervals, group_indices

    def get_groups(self):
        ''' return list of dictionaries, for each partition group dict looks like
            { 'intervals': [(2, 5), (9, 11), .., (0, 4), (2, 2)], 'indices': [3, 7, 27, ..] }
            with intervals: a list yielding for each qi column (min, max)-values of the partition
            and indices: providing the indices of the initial dataframe's rows belonging to partition'''
        partitions_info = []
        for part in self.result:
            group_intervals, group_indices = self.group_to_partition(part)
            partitions_info.append( { 'intervals': group_intervals, 'indices': group_indices } )
        #print('\n FINAL GROUP LIST, some values: \n %s \n' % partitions_info[:4])
        return partitions_info

    def convert_back(self, col, col_range):
        cat_dict = self.data.category_dict
        if col in cat_dict:
            try:
                min, max = col_range
                col_range = tuple(cat_dict[col][min: max+1])
                ## ! TODO: The next line makes tuples to single string containing all its values listed
                # (better for writing to file)
                # col_range = ','.join(col_range)
            except TypeError:
                # there is no range of values for column col, only one value
                val = col_range
                col_range = cat_dict[col][val]
        return col_range

    def to_frame(self, group, convert=False):
        ''' return dataframe to a group dictionary'''
        indices = group['indices']
        intervals = group['intervals']
        frame = self.data.records.T[indices].T
        for i, col in enumerate(frame):
            if i >= len(intervals):
                # no transformation of the last/ sensible column
                continue
            col_range = intervals[i]
            if col_range[0] == col_range[1]:
                col_range = col_range[0]
            if convert:
                col_range = self.convert_back(col, col_range)
            frame[col] = str(col_range)
        return frame

    def anonym_frame(self, convert=False):
        ''' if convert = True, convert back category columns'''
        groups = self.get_groups()
        frames = []
        for group in groups:
            frame = self.to_frame(group, convert)
            frames.append(frame)
        anonym_frame = pd.concat(frames)
        return anonym_frame

    def col_indices(self, x_col=0, y_col=1, column_names=None):
        if not column_names:
            column_names = list(self.data.column_names)
        dims = [x_col, y_col]
        for i, dim in enumerate(dims):
            try:
                dims[i] = column_names.index(dim)
                # x_col/ y_col is valid col name and dims[i] now its index
            except ValueError:
                # no valid x_col/ y_col name is given
                try:
                    dims[i] = int(dim)
                    # dim is integer, check whether it points to some index of column_names
                    if dim >= 0 or dim < len(column_names):
                        # valid x_col/ y_col index given
                        dims[i] = dim
                except ValueError:
                    # no valid x_col/ y_col index given, use index of first/ second column of frame
                    dims[i] = i
        return tuple(dims)

    def plot_dict(self, groups, x_index, y_index):
        # Note: x_coords is still list of length qi_length, every entry being a tuple of 
        # x_min, x_max values, not a proper coordinate tuple
        x_coords = [ group['intervals'][x_index]  for group in groups ]
        y_coords = [ group['intervals'][y_index]  for group in groups ]
        # find the global mins/ max of the data
        xcoords_separate = list(zip(*x_coords))
        ycoords_separate = list(zip(*y_coords))
        global_xmin = min(xcoords_separate[0])
        global_xmax = max(xcoords_separate[1])
        global_ymin = min(ycoords_separate[0])
        global_ymax = max(ycoords_separate[1])
        return { 'x': x_coords, 'y': y_coords, 'border_x': (global_xmin, global_xmax), 
                    'border_y': (global_ymin, global_ymax)}

    def plot_anonym(self, x_col=0, y_col=1, groups=None, data=True, 
            out_dir='./images/', filename='out.png'):
        ''' plot the 2D mondrian regions dim0 = x_col, dim1 = y_col.
            input options:
            * both columns: by name or index of col, 
              else: use first and second column of dataframe
            * groups: if not given, compute anonym groups from self.results
            * data: if True, also plot data points inside areas
            * out_dir, filename: possibly specify in which directory and/ or 
                        under which name the image file shall be stored '''
        if not groups:
            groups = self.get_groups()
        x_index, y_index = self.col_indices(x_col=x_col, y_col=y_col)
        # get the required info to plot for all regions
        plot_dict = self.plot_dict(groups, x_index, y_index)
        x_coords = plot_dict['x']
        y_coords = plot_dict['y']
        global_xmin, global_xmax = plot_dict['border_x']
        global_ymin, global_ymax = plot_dict['border_y']
        # start figure
        fig = plt.figure()
        fig_plot = fig.add_subplot(1, 1, 1)
        # tick space defines which axis labels are printed (here: every second value)
        tick_spacing = 2
        fig_plot.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        currentAxis = plt.gca()
        # draw a rectangle around all data
        currentAxis.add_patch(Rectangle( (global_xmin, global_ymin), (global_xmax-global_xmin), 
                                (global_ymax-global_ymin), edgecolor='yellow', facecolor='none' ))
        # iteratively plot anonym regions
        for i in range(len(x_coords)):
            xmin, xmax = x_coords[i]
            ymin, ymax = y_coords[i]
            ## TODO: offset should fit until next value starts 
            offset_x, offset_y = 1, 1
            if xmax == global_xmax:
                offset_x = 0
            if ymax == global_ymax:
                offset_y = 0
            # draw regions as almost transparent rectangles 
            currentAxis.add_patch(Rectangle((xmin, ymin), (xmax-xmin+offset_x), (ymax-ymin+offset_y), alpha=0.1, facecolor='grey'))
            # draw bottom and left borders of every region
            fig_plot.plot([xmin, xmin, xmin, xmax+offset_x], [ymin, ymax+offset_y, ymin, ymin], color=(0.46,0.46,0.46,1))
        # if True, also draw all datapoints inside their regions
        # use different color dependent upon the data point's value
        if data:
            sensible_data = self.data.records.ix[:, -1]
            sensible_uniques = sensible_data.unique()
            N = len(sensible_uniques)
            # use some colormap for N different colors 
            cmap = plt.get_cmap('brg')
            for i, value in enumerate(sensible_uniques):
                color = cmap((float(i)/N))
                # for every different sensible value get all its indices
                # and plot the corresponding data points in the current color
                value_indices = sensible_data[ sensible_data == value ].index
                xcol_data = self.data.records.ix[value_indices, x_index]
                ycol_data = self.data.records.ix[value_indices, y_index]
                fig_plot.plot(xcol_data, ycol_data, '.', color=color, markersize=3)
        # set path to directory to store images
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        # get current time
        time_now = time.strftime('%d.%m.%Y_%H.%M.%S')
        # if filename has already a file ending, remove it
        ## TODO: actually one could (should?) use only the given filename without time
        name_split = filename.rsplit('.')
        if len(name_split) > 1:
            filename = name_split[0]
        # set path to the file
        filepath = os.path.join('./images/', '%s_%s.pdf' % (filename, time_now))
        plt.savefig(filepath)
        print('Save image to file %s .' %filepath)
        # TODO: maybe better don't show picture always
        plt.show()


    def write_frame(self, frame, out_dir='./', filename=None):
        ## TODO: convert tuples to a string that lists all values
        if not filename:
            current_time = time.strftime('%d.%m.%Y_%H.%M.%S')
            filename = 'out_%s.csv' % current_time
        assert(os.path.isdir(out_dir)), 'No valid out directory given: %s .' % out_dir
        path = os.path.join(out_dir, filename)
        frame.to_csv(path, sep=';', index=False)
        print('Written anonym data to file %s .' %path)


if __name__ == '__main__':

    mondrian = Mondrian(k=6, l=3)
    data = NumpyDataSet(data=load_csv('data/adult_klein.data'),
                        meta=parse_yaml('data/adult_plot.yaml'))


    data[0,:1000]

    result = mondrian.anonymize(data)

    newMondrian = Mondrian('data/adult_plot.yaml', 'data/adult_klein.data')
    #info = newMondrian.get_groups()
    print('\n RESULT:')
    anonym_frame = newMondrian.anonym_frame(convert=False)
    #print('\n anonym frame: \n %s' %anonym_frame.sample(20))
    newMondrian.write_frame(anonym_frame)
    print('\n PLOT:')
    newMondrian.plot_anonym()
    print('\n \n FINISHED!')

