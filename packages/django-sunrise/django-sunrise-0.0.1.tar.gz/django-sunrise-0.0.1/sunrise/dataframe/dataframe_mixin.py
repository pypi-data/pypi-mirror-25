""" Dataframe Manager """
# Author: Partha

import pandas as pd


class DataFrameManager(object):
    """ Manages queryset using pandas functionalities """
    model = None
    qset = None

    def __init__(self, *args, **kwargs):
        if 'queryset' in kwargs:
            self.qset = kwargs['qset']
        elif 'model' in kwargs:
            self.model = kwargs['model']
            self.qset = self.model.objects.all()
        else:
            if self.model is not None:
                self.qset = self.model.objects.all()

    def queryset_to_cache_df(
            self,
            queryset=None,
            reset=False
    ):
        """ Used to conver the queryset to dataframe"""
        #1. Finding queryset
        if queryset is None:
            if qset is None:
                return (False, "QuerySet Not Found")
        else:
            self.qset = queryset
        master = []
        modified = []
        count = 0
        if reset is False:
            payload = self.qset.values()
        if reset is True:
            payload = self.qset
        for item in payload:
            _master_item = item.copy()
            _master_item.update({'grid_index': count})
            temp = dict()
            for key, value in item.items():
                temp[key] = (value, 'bound') ##changed here
            temp['grid_index'] = count
            temp['row_bound_status'] = 'bound'
            temp['row_added_status'] = False
            count = count + 1
            modified.append(temp)
            master.append(_master_item)
        return (pd.DataFrame(master), pd.DataFrame(modified), payload)

    def sort_by(
            self,
            dataframe_,
            column,
            asc=True
    ):
        """ Used to sort the dataframe """
        dataframe_.sort(columns=[column], ascending=asc)


class CacheDataFrameManager(DataFrameManager):
    """ Used to manage the data """
    model = None
    qset = None

    def array_to_data_frame(
            self,
            array_
    ):
        """ Convert array to data frame """
        return pd.DataFrame(array_)

    def append_array(
            self,
            dataframe_,
            array_data
    ):
        """ Append arr to dataframe df """
        temp_data_frame = pd.DataFrame(array_data)
        dataframe_ = df.append(temp_data_frame, ignore_index=True)
        return dataframe_

    def insert_row(
            self,
            frame,
            new,
            row
    ):
        """ Will insert a new row at specified index """
        new = pd.DataFrame(new)
        if frame is not None and len(frame.index) > 0:
            #1. Get index using grid index
            currentindex = frame.loc[frame['grid_index'] == row].index.values[0] + 1
            top = frame[0:currentindex]
            bottom = frame[currentindex:]
            return pd.concat((top, new, bottom)).reset_index(drop=True)
        return new

class MultiResourceDataFrameManager(DataFrameManager):
    """ Used for managing custom data """
    data = None

    def build_data(
            self,
            data=None,
            fields=None
    ):
        """ To convert the qset or list of values
        into dataframe """
        try:
            dataframe_ = pd.DataFrame(data, columns=fields)
            dataframe_['grid_index'] = dataframe_.index
        except Exception, general_exception:
            return (False, None)
        return (True, dataframe_)
