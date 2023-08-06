""" Cache Module """
# Author: Partha

from datetime import datetime

import StringIO
import pandas as pd
import pytz

from django.core.cache import caches
from sunrise.dataframe.dataframe_mixin import (CacheDataFrameManager,
                                               MultiResourceDataFrameManager)

CACHE = caches['default']


class BaseCache(object):
    """ Generic functionality to handle the cache """

    model = None
    serializer = None
    qset = None

    def __init__(
            self,
            *args,
            **kwargs
    ):
        if "model" in kwargs:
            self.model = kwargs['model']
        if 'serializer' in kwargs:
            self.serializer = kwargs['serializer']
        if 'qset' in kwargs:
            self.qset = kwargs['qset']

    def set(
            self,
            key,
            data=None
    ):
        """ Will set the data into the specified key """
        try:
            CACHE.set(key, data)
            return True
        except Exception, general_exception:
            return False

    def get(
            self,
            key
    ):
        """ Will retrieve the data with the specified keys """
        try:
            return CACHE.get(key)
        except Exception, general_exception:
            return None

    def delete_pattern(
            self,
            pattern
    ):
        """ Will delete the keys based on specified pattern """
        try:
            return CACHE.delete_pattern(pattern)
        except Exception, general_exception:
            return None


class PageCache(BaseCache):
    """ To maintain page level cache elements """

    cache_key = None
    cache_key_initial_data = None
    cache_key_parent_pk = None
    cache_key_search_key = None
    cache_key_search_list = None
    cache_key_return_criteria = None

    def initiate(
            self,
            uuid_hash=None
    ):
        """ This will create env keys for page level """
        if self.cache_key is None:
            self.cache_key = uuid_hash
        self.cache_key_initial_data = self.cache_key + "_initial_data"
        self.cache_key_parent_pk = self.cache_key + "_parent_pk"
        self.cache_key_search_key = self.cache_key + "_search_key"
        self.cache_key_search_list = self.cache_key + "_search_list"
        self.cache_key_return_criteria = self.cache_key + "_return_criteria"
        return self

    def set_initial_data(
            self,
            data
    ):
        """ Used to set the initial data """
        self.set(
            self.cache_key_initial_data,
            data
        )
        return True

    def get_initial_data(
            self
    ):
        """ Used to get the initial data """
        return self.get(self.cache_key_initial_data)

    def set_parent_pk(
            self,
            primary_key=None
    ):
        """ Used to set the parent pk """
        self.set(self.cache_key + "_parent_pk", pk)
        return pk

    def get_parent_pk(
            self
    ):
        """ Used to return the primary key """
        return self.get(self.cache_key + "_parent_pk")

    def set_search_key(
            self,
            key
    ):
        """ This is used to point the next key and set it as current key """
        try:
            key = int(key)
        except Exception, general_exception:
            pass
        _list = self.get_search_list()
        idx = _list.index(key)
        self.set(self.cache_key_parent_pk, key)
        self.set(self.cache_key_search_key, idx)

    def get_search_key(
            self
    ):
        """ This will get the current search primary key """
        current_index = int(self.get_current_index())
        _list = self.get_search_list()
        _list_length = len(_list)
        _has_next = True if current_index + 1 <= _list_length - 1 else False
        _has_prev = True if (current_index - 1) >= 0 else False
        return (_list[current_index], _has_prev, _has_next)

    def set_search_list(
            self,
            key,
            _grid_cache_key
    ):
        """ This is used to set the search keys for
        prev/next/return purpose """
        data = self.get(self.get(_grid_cache_key))
        _list = []
        if len(data) > 0:
            _list = data[key].tolist()
        self.set(self.cache_key_search_list, _list)

    def get_search_list(
            self
    ):
        """ To return the list of search keys """
        return self.get(self.cache_key_search_list)

    def get_current_index(
            self
    ):
        """ This is used to get the current index from the search list """
        return self.get(self.cache_key_search_key)

    def get_next_key(
            self
    ):
        """ This is used to get the next key from search results """
        current_index = int(self.get_current_index())
        _list = self.get_search_list()

        _list_length = len(_list)
        if current_index < _list_length:
            current_index += 1
            self.set(self.cache_key_search_key, current_index)
            self.set(self.cache_key + "_parent_pk", _list[current_index])
        else:
            current_index = None
        _has_next = True if current_index + 1 < _list_length else False
        _has_prev = True if (current_index) >= 1 else False
        return (_list[current_index], _has_prev, _has_next)

    def get_prev_key(
            self
    ):
        """ This is used to get the prev key from the search list """
        current_index = int(self.get_current_index())
        _list = self.get_search_list()
        _list_length = len(_list)
        if current_index >= 1:
            current_index -= 1
            self.set(self.cache_key_search_key, current_index)
            self.set(self.cache_key + "_parent_pk", _list[current_index])
        else:
            current_index = None
        _has_next = True if current_index + 1 < _list_length else False
        _has_prev = True if (current_index) >= 1 else False
        return (_list[current_index], _has_prev, _has_next)

    def set_return_criteria(
            self,
            data
    ):
        """ Used to set the return criteria """
        self.set(self.cache_key_return_criteria, data)
        return True

    def get_return_criteria(
            self
    ):
        """ Used to get the return criteria """
        return self.get(self.cache_key_return_criteria)


class ResourceCache(BaseCache):
    """ Used for caching the Resource/Webservice """
    cache_key = None
    cache_key_queryset = None
    cache_key_master = None
    cache_key_slave = None
    cache_key_modified = None
    cache_key_sorted = None
    cache_key_filtered = None
    cache_key_deleted = None
    cache_key_criteria = None
    cache_key_active = None

    def __init__(
            self,
            *args,
            **kwargs
    ):
        """ Initiating grid cache keys and cache state keys """
        uuid_hash = kwargs['uuid_hash']
        if 'GRID_KEY' in kwargs.keys() and kwargs['GRID_KEY'] is not None:
            uuid_hash = uuid_hash + "_" + kwargs['GRID_KEY']
        self._init_cache_state_keys(uuid_hash)
        super(ResourceCache, self).__init__(*args, **kwargs)

    def _init_cache_state_keys(
            self,
            uuid_hash
    ):
        """ This is used to initiate/maintain the refs to cache keys """
        self.cache_key = uuid_hash
        self.cache_key_queryset = self.cache_key + "_queryset"
        self.cache_key_master = self.cache_key + "_master"
        self.cache_key_slave = self.cache_key + "_slave"
        self.cache_key_modified = self.cache_key + "_modified"
        self.cache_key_sorted = self.cache_key + "_sorted"
        self.cache_key_filtered = self.cache_key + "_filtered"
        self.cache_key_deleted = self.cache_key + "_deleted"
        self.cache_key_criteria = self.cache_key + "_criteria"
        self.cache_key_active = self.cache_key + "_active"
        return True

    def register_cache_state_keys(
            self
    ):
        """ To build cache keys required to hold the replicas of data """
        # Creating cachekey with data None
        map(self.set, [self.cache_key_master,
                       self.cache_key_modified,
                       self.cache_key_sorted,
                       self.cache_key_filtered,
                       self.cache_key_slave,
                       self.cache_key_deleted,
                       self.cache_key_criteria
                      ])
        return True

    def _get_active_cache_key(
            self
    ):
        """ Used to return the key from which cache_key the data is returned """
        return self.get(self.cache_key_active)

    def _get_active_cache_data(
            self
    ):
        """ Used to return the data from the current active Cache """
        return self.get(self._get_active_cache_key())

    def get_page_data(
            self,
            grid_index,
            range
    ):
        """ Used to return the offset range of activeCacheData """
        _active_data = self._get_active_cache_data()
        total_num = len(self.get_data())
        if grid_index == -1:
            currentindex = 0
            start_num = currentindex
            try:
                active_data = _active_data.loc[_active_data.index >= 0][:range]
                end_num = currentindex + len(active_data.index)
            except Exception, general_exception:
                active_data = _active_data.loc[_active_data.index >= 0][:]
                end_num = currentindex + len(active_data.index)
        else:
            if grid_index == -9999:
                currentindex = 0
                try:
                    active_data = _active_data.loc[_active_data.index >= 0][-range:]
                    end_num = len(_active_data.index)
                    start_num = end_num - range
                    if start_num < 0:
                        start_num = 0
                    currentindex = start_num
                except Exception, general_exception:
                    active_data = _active_data.loc[_active_data.index >= 0][:]
                    end_num = len(_active_data.index)
                    start_num = len(active_data.index)
                    currentindex = start_num
            else:
                currentindex = _active_data.loc[_active_data['grid_index']
                                                == grid_index].index.values[0]
                start_num = currentindex + 1
                try:
                    active_data = _active_data.loc[_active_data.index >
                                                   currentindex][:range]
                    end_num = currentindex + len(active_data.index) + 1
                except Exception, general_exception:
                    active_data = _active_data.loc[_active_data.index >
                                                   currentindex][:]
                    end_num = currentindex + len(active_data.index) + 1
        try:
            next_low_bound = _active_data.loc[_active_data.index > currentindex].to_dict(
                orient="records")[range]['grid_index']
        except Exception, general_exception:
            next_low_bound = None
        try:
            prev_low_bound = _active_data.loc[_active_data.index < currentindex].to_dict(
                orient="records")[-(range)]['grid_index']
        except Exception, general_exception:
            prev_low_bound = -1
        return (
            active_data.to_dict(orient='records'),
            prev_low_bound,
            next_low_bound,
            start_num,
            end_num,
            total_num
        )

    def _set_active_cache_key(
            self,
            key
    ):
        """ Used to set the active cache key """
        self.set(self.cache_key_active, key)

    def ceil_cache(
            self
    ):
        """ It is used to set the cache keys(modified, deleted) data to None """
        keys = [self.cache_key_deleted]
        # here need to update unbound to bound
        for key in keys:
            self.set(key, None)
        return True

    def set_grid_cache_data(
            self,
            qset=None,
            model=None
    ):
        """ Invoked when first time data is loading """
        # 1. input validation for better usage
        if qset is None and model is None and self.qset is None and self.model is None:
            return (False, "Model or Queryset Not Found")
        elif qset is not None:
            self.qset = qset
        elif model is not None:
            self.qset = model.objects.all()
        # 2. Initiate DataFrameManager
        data_frame_ref = CacheDataFrameManager()
        master_data, modified_data, oqset = data_frame_ref._querysetToCacheDf(self.qset)
        # 3. Syncing master, slave, modified caches
        self.set(self.cache_key_queryset, oqset)
        self.set(self.cache_key_master, master_data)
        self.set(self.cache_key_slave, master_data)
        self.set(self.cache_key_modified, modified_data)
        # 4. Setting active cache_key
        self._set_active_cache_key(self.cache_key_slave)

    def set_search_params(
            self,
            data
    ):
        """ This is used to set the search params """
        self.set(self.cache_key_criteria, data)
        return True

    def get_search_params(
            self
    ):
        """ This is used to get the search params """
        return self.get(self.cache_key_criteria)

    def add_item(
            self,
            at_grid_index,
            fields
    ):
        """ Hook invoked when add item triggered """
        # 1. Get the slave data and its length, and get modified data
        # import pdb;pdb.set_trace()
        master_data = self.get(self.cache_key_master)
        slave_data = self.get(self.cache_key_slave)
        modified_data = self.get(self.cache_key_modified)
        deleted_data = self.get(self.cache_key_deleted)
        # 2. baking grid index
        try:
            grid_index = modified_data.loc[modified_data['grid_index'].idxmax(
            )].grid_index + 1  # len(master_data.index)
        except Exception, general_exception:
            grid_index = 0
        if deleted_data is not None:
            grid_index = grid_index + len(deleted_data)
        if len(slave_data) == 0:
            at_grid_index = 0
            # grid_index = 0
        at_grid_index = int(at_grid_index)
        # 3. Adding an empty row with grid index to modified and slave with emmpty values
        temp = {key: '' for key in fields}
        temp.update({'grid_index': grid_index})
        temp_dataframe = CacheDataFrameManager()
        slave_data = temp_dataframe.insertRow(slave_data, [temp], at_grid_index)
        self.set(self.cache_key_slave, slave_data)
        # 4. Syncing to active cache
        if self._get_active_cache_key() != self.cache_key_slave:
            active_data = self._get_active_cache_data()
            active_data = temp_dataframe.insertRow(active_data, [temp], at_grid_index)
            self.set(self._get_active_cache_key(), active_data)
        # 5. Adding the slave data to modified
        temp = {key: (None, 'unbound') for key in fields}
        temp.update({'grid_index': grid_index,
                     'row_bound_status': 'unbound', 'row_added_status': True})
        modified_data = temp_dataframe.insertRow(modified_data, [temp], at_grid_index)
        self.set(self.cache_key_modified, modified_data)
        # 6. Returning the grid index
        return grid_index

    def delete_item(
            self,
            grid_index,
            low_bound
    ):
        """ Invoked when delete item occurs """
        # 1. Get the row using grid_index from the activeCache
        active_data = self._get_active_cache_data()
        modified_data = self.get(self.cache_key_modified)
        active_row = active_data.loc[active_data['grid_index'] == grid_index]
        low_bound_row = None
        low_bound_next = None
        if low_bound is not None:
            low_bound_row = active_data.loc[active_data['grid_index'] == int(
                low_bound)].index.values[0]
            try:
                next_row = active_data.ix[low_bound_row + 1].to_dict()
            except Exception, general_exception:
                next_row = None
        else:
            next_row = None

        if low_bound_row is not None and next_row is not None:
            try:
                low_bound_next = active_data.ix[low_bound_row + 2]['grid_index']
            except Exception, general_exception:
                low_bound_next = None
        deleted_data = self.get(self.cache_key_deleted)
        if deleted_data is not None:
            self.set(self.cache_key_deleted, deleted_data.append(
                active_row, ignore_index=True))
        else:
            self.set(self.cache_key_deleted, active_row)
        # 2. Delete the row from the activeCache
        active_data = active_data.query('grid_index != ' + grid_index.__str__())
        # 3. Delete the row from the modifiedCache
        if modified_data is not None:
            modified_data = modified_data.query(
                'grid_index != ' + grid_index.__str__())
            modified_data = modified_data.reset_index(drop=True)
        # 4. Save back to cache
        active_data = active_data.reset_index(drop=True)
        self.set(self._get_active_cache_key(), active_data)
        self.set(self.cache_key_modified, modified_data)
        return (next_row, low_bound_next)

    def update_item(
            self,
            data
    ):
        """ Adding new/modified data into the slave and modified """
        material_keys = ["grid_index", "row_changed",
                         "newly_added", "can_add_only"]
        # 1. Getting slave and modified data
        slave_data = self.get(self.cache_key_slave)
        modified_data = self.get(self.cache_key_modified)
        if self._get_active_cache_key() != self.cache_key_slave:
            active_data = self._get_active_cache_data()
        else:
            active_data = None
        # 2. Updating slave and modified data using grid_index
        # I know, but it is better repeat the code here(less condition checking)
        if active_data is None:
            for row in data:
                for key, value in row.items():
                    if key not in material_keys:
                        try:
                            slave_data.loc[slave_data['grid_index']
                                           == row['grid_index'], key] = value
                            idx = modified_data.loc[modified_data['grid_index'] == row['grid_index'], key].index.tolist()[
                                0]
                            ret_data = modified_data.get_value(
                                idx, key)  # changed here
                            if type(ret_data) == tuple:
                                if ret_data[0] != value:
                                    modified_data.set_value(
                                        idx, key, (value, 'unbound'))  # changed here
                        except KeyError:
                            pass
                        except ValueError:
                            if value is not None:
                                try:
                                    value = datetime.strptime(
                                        value, '%m/%d/%Y').replace(tzinfo=pytz.utc)
                                    slave_data.loc[slave_data['grid_index']
                                                  == row['grid_index'], key] = value
                                    idx = modified_data.loc[modified_data['grid_index'] == row['grid_index'], key].index.tolist()[
                                        0]
                                    ret_data = modified_data.get_value(
                                        idx, key)  # changed here
                                    if type(ret_data) == tuple:
                                        if ret_data[0] != value:
                                            modified_data.set_value(
                                                idx, key, (value, 'unbound'))  # changed here
                                except Exception, general_exception:
                                    print "---------Exception:-------"
                                    print str(e)
                        except Exception, general_exception:
                            print "---------Exception:-------"
                            print str(e)

                modified_data.loc[modified_data['grid_index'] ==
                                 row['grid_index'], 'row_bound_status'] = 'unbound'
            self.set(self.cache_key_slave, slave_data)
            self.set(self.cache_key_modified, modified_data)
        else:
            for row in data:
                for key, value in row.items():
                    try:
                        slave_data.loc[slave_data['grid_index']
                                      == row['grid_index'], key] = value
                        active_data.loc[active_data['grid_index']
                                       == row['grid_index'], key] = value
                        idx = modified_data.loc[modified_data['grid_index'] == row['grid_index'], key].index.tolist()[
                            0]
                        ret_data = modified_data.get_value(
                            idx, key)  # changed here
                        if type(ret_data) == tuple:
                            if ret_data[0] != value:
                                modified_data.set_value(
                                    idx, key, (value, 'unbound'))  # changed here
                    except KeyError:
                        pass
                    except ValueError:
                        if value is not None:
                            try:
                                value = datetime.strptime(
                                    value, '%m/%d/%Y').replace(tzinfo=pytz.utc)
                                slave_data.loc[slave_data['grid_index']
                                              == row['grid_index'], key] = value
                                active_data.loc[active_data['grid_index']
                                               == row['grid_index'], key] = value
                                idx = modified_data.loc[modified_data['grid_index'] == row['grid_index'], key].index.tolist()[
                                    0]
                                ret_data = modified_data.get_value(
                                    idx, key)  # changed here
                                if type(ret_data) == tuple:
                                    if ret_data[0] != value:
                                        modified_data.set_value(
                                            idx, key, (value, 'unbound'))  # changed here
                            except Exception, general_exception:
                                print "---------Exception:-------"
                                print str(e)
                    except Exception, general_exception:
                        print "---------Exception:-------"
                        print str(e)
                modified_data.loc[modified_data['grid_index'] ==
                                 row['grid_index'], 'row_bound_status'] = 'unbound'
            self.set(self.get(self.cache_key_active), active_data)
            self.set(self.cache_key_modified, modified_data)
            self.set(self.cache_key_slave, slave_data)
        return True

    def search_cache(
            self,
            **filters
    ):
        """ Used to filter over slave and return from the slave """
        # 1. Read the slave_data
        slave_data = self.get(self.cache_key_slave)
        # 2. filter the slave_data with filter attributes and sync it to the filtered cache
        filtered_data = slave_data
        for key, val in filters.items():
            filtered_data = filtered_data[([key] == val)]
        # 3. syncing filtereData with the result
        self.set(self.cache_key_filtered, filtered_data)
        # 4. Setting active cache key as filtered_keye
        self._set_active_cache_key(cache_key_filtered)
        # 5. Returning the filtered_data
        return self.get(self.cache_key_filtered)

    def refresh_cache(
            self
    ):
        """ This is used to reset the cache state to initial """
        # 1. Get the Queryset from Cache
        qset = self.get(self.cache_key_queryset)
        data_frame_ref = CacheDataFrameManager()
        master_data, modified_data, oqset = data_frame_ref._querysetToCacheDf(
            qset, reset=True)
        # 3. Syncing master, slave, modified caches
        self.set(self.cache_key_queryset, oqset)
        self.set(self.cache_key_master, master_data)
        self.set(self.cache_key_slave, master_data)
        self.set(self.cache_key_modified, modified_data)
        # 4. Setting active cache_key
        self._set_active_cache_key(self.cache_key_slave)

    def sort_cache(
            self,
            column,
            asc
    ):
        """ Used to sort the active cache(filtered/slave) """
        # 1. Sorting the data frame based on column
        sorted_data = self.get(self._get_active_cache_key()).sort(
            columns=[column], ascending=asc).reset_index(drop=True)
        # 2. Making active cachekey as sorted cache key
        self._set_active_cache_key(self.cache_key_sorted)
        # 3. syncing sorted_data with cache_key_filtered
        self.set(self.cache_key_sorted, sorted_data)
        # 4. Returning active Data(now it is sorted data)
        return self.get_data()

    def set_stable_state(
            self,
            pk_container=None
    ):
        """ Used to reset the cache state on Save/Update """
        # 1. Removed _deleted
        self.set(self.cache_key_deleted, None)
        # 2. Set row_bound_status to 'bound' of _modified
        modified_data = self.get(self.cache_key_modified)
        slave_data = self.get(self.cache_key_slave)
        if self._get_active_cache_key() != self.cache_key_slave:
            active_data = self._get_active_cache_data()
        else:
            active_data = None
        if len(modified_data) != 0 and modified_data is not None:
            for item in self.items_to_update:
                for key, val in item.items():
                    idx = modified_data.loc[modified_data['grid_index'] == item['grid_index'], key].index.tolist()[
                        0]
                    ret_data = modified_data.get_value(idx, key)
                    if isinstance(ret_data, tuple) is True:
                        modified_data.set_value(
                            idx, key, (val, 'bound'))  # changed here

            for item in self.items_to_add:
                # Updating pk's to the cache

                if item['grid_index'] in pk_container.keys():
                    # Updating added items 'pk' to the slave/active cache to get reflected
                    _midx = modified_data.loc[modified_data['grid_index'] == item['grid_index'], 'id'].index.tolist()[
                        0]
                    modified_data.set_value(
                        _midx, 'id', (pk_container[item['grid_index']], 'bound'))
                    # Updating pks to slave
                    _sidx = slave_data.loc[slave_data['grid_index'] == item['grid_index'], 'id'].index.tolist()[
                        0]
                    slave_data.set_value(
                        _sidx, 'id', pk_container[item['grid_index']])

                    # Updating pks to activeCache
                    if active_data is not None:
                        _aidx = active_data.loc[active_data['grid_index'] == item['grid_index'], 'id'].index.tolist()[
                            0]
                        active_data.set_value(
                            _aidx, 'id', pk_container[item['grid_index']])

            # 3. Set row_added_status to 'False' of _modified
            modified_data.loc[:, 'row_bound_status'] = 'bound'
            modified_data.loc[:, 'row_added_status'] = False
            self.set(self.cache_key_modified, modified_data)
            self.set(self.cache_key_slave, slave_data)
            if active_data is not None:
                self.set(self._get_active_cache_key(), active_data)
        return True

    def get_data(
            self
    ):
        """ Used to retrieve the data from the cache based on unikKey + self.cache_key"""
        # Returning the data from the active cache key
        active_data = self._get_active_cache_data()
        return active_data.to_dict(orient='records')

    def get_data_as_csv(
            self
    ):
        """ Used to return dataframe as csv """
        active_data = self._get_active_cache_data()
        return active_data.to_csv()

    def get_data_as_xls(
            self
    ):
        """ Used to return the data as xlsx """
        import StringIO
        sio = StringIO.StringIO()
        pandas_writer = pd.ExcelWriter(sio, general_exceptionngine='xlsxwriter')
        active_data = self._get_active_cache_data()
        # Create excel file here manually by serializing the fields
        active_data.to_excel(pandas_writer, sheet_name="download")
        pandas_writer.save()
        sio.seek(0)
        workbook = sio.getvalue()
        return workbook

    def delete_cache(
            self
    ):
        self.delete_pattern(self.cache_key + "_")

    @property
    def debug(
            self
    ):
        """ Enabling developers to see the backend transperantly """
        return {
            'items_to_add': self.items_to_add,
            'items_to_update': self.items_to_update,
            'items_to_delete': self.items_to_delete,
            'rows_added': len(self.items_to_add),
            'rows_changed': len(self.items_to_update),
            'rows_deleted': len(self.items_to_delete)
        }

    @property
    def items_to_add(
            self
    ):
        """ returns a list of items to add """
        modified_data = self.get(self.cache_key_modified)
        if modified_data is not None and len(modified_data) > 0:
            added_data = modified_data.loc[modified_data['row_added_status'] == True]
            if added_data is not None:
                return added_data.to_dict(orient='records')
            else:
                return []
        else:
            return []

    @property
    def items_to_delete(
            self
    ):
        """ returns a list of items to be deleted """
        deleted_data = self.get(self.cache_key_deleted)
        if deleted_data is not None and len(deleted_data) > 0:
            return deleted_data.to_dict(orient='records')
        else:
            return []

    @property
    def items_to_update(
            self
    ):
        """ returns a list of items to be updated """
        modified_data = self.get(self.cache_key_modified)
        if modified_data is not None and len(modified_data.index) > 0:
            modified_data = modified_data.loc[(modified_data['row_bound_status'] == 'unbound') & (
                modified_data['row_added_status'] == False)]
            if modified_data is not None:
                return modified_data.to_dict(orient='records')
            else:
                return []
        else:
            return []


class MultiResourceCache(BaseCache):
    """ Used to cache the remote api Resources """
    cache_key = None
    cache_key_queryset = None
    cache_key_master = None
    cache_key_slave = None
    cache_key_modified = None
    cache_key_sorted = None
    cache_key_filtered = None
    cache_key_deleted = None
    cache_key_criteria = None
    cache_key_active = None

    def __init__(
            self,
            *args,
            **kwargs
    ):
        """ Initiating grid cache keys and cache state keys """
        uuid_hash = kwargs['uuid_hash']
        if 'GRID_KEY' in kwargs.keys() and kwargs['GRID_KEY'] is not None:
            uuid_hash = uuid_hash + "_" + kwargs['GRID_KEY']
        self._init_cache_state_keys(uuid_hash)
        super(MultiResourceCache, self).__init__(*args, **kwargs)

    def _init_cache_state_keys(
            self,
            uuid_hash
    ):
        """ This is used to initiate/maintain the refs to cache keys """
        self.cache_key = uuid_hash
        self.cache_key_master = self.cache_key + "_master"
        self.cache_key_slave = self.cache_key + "_slave"
        self.cache_key_sorted = self.cache_key + "_sorted"
        self.cache_key_criteria = self.cache_key + "_criteria"
        self.cache_key_active = self.cache_key + "_active"
        return True

    def register_cache_state_keys(
            self
    ):
        """ To build cache keys required to hold the replicas of data """
        # Creating cachekey with data None
        map(self.set, [
            self.cache_key_master,
            self.cache_key_sorted,
            self.cache_key_slave,
            self.cache_key_criteria,
        ])
        return True

    def _get_active_cache_key(
            self
    ):
        """ Used to return the key from which cache_key the data is returned """
        return self.get(self.cache_key_active)

    def _get_active_cache_data(
            self
    ):
        """ Used to return the data from the current active Cache """
        return self.get(self._get_active_cache_key())

    def get_page_data(
            self,
            grid_index,
            range
    ):
        """ Used to return the offset range of activeCacheData """
        _active_data = self._get_active_cache_data()
        total_num = len(self.get_data())
        if grid_index == -1:
            currentindex = 0
            start_num = currentindex
            try:
                active_data = _active_data.loc[_active_data.index >= 0][:range]
                end_num = currentindex + len(active_data.index)
            except Exception, general_exception:
                active_data = _active_data.loc[_active_data.index >= 0][:]
                end_num = currentindex + len(active_data.index)
        else:
            if grid_index == -9999:
                currentindex = 0
                try:
                    active_data = _active_data.loc[_active_data.index >= 0][-range:]
                    end_num = len(_active_data.index)
                    start_num = end_num - range
                    currentindex = start_num
                except Exception, general_exception:
                    active_data = _active_data.loc[_active_data.index >= 0][:]
                    end_num = len(_active_data.index)
                    start_num = len(active_data.index)
                    currentindex = start_num
            else:
                currentindex = _active_data.loc[_active_data['grid_index']
                                               == grid_index].index.values[0]
                start_num = currentindex + 1
                try:
                    active_data = _active_data.loc[_active_data.index >
                                                 currentindex][:range]
                    end_num = currentindex + len(active_data.index) + 1
                except Exception, general_exception:
                    active_data = _active_data.loc[_active_data.index >
                                                 currentindex][:]
                    end_num = currentindex + len(active_data.index) + 1
        try:
            next_low_bound = _active_data.loc[_active_data.index >= currentindex].to_dict(
                orient="records")[range]['grid_index']
        except Exception, general_exception:
            next_low_bound = None
        try:
            prev_low_bound = _active_data.loc[_active_data.index < currentindex].to_dict(
                orient="records")[-(range)]['grid_index']
        except Exception, general_exception:
            prev_low_bound = -1
        return (active_data.to_dict(orient='records'), prev_low_bound, next_low_bound, start_num, general_exceptionnd_num, total_num)

    def _set_active_cache_key(
            self,
            key
    ):
        """ Used to set the active cache key """
        self.set(self.cache_key_active, key)

    def set_grid_cache_data(
            self,
            data=None,
            fields=None
    ):
        """ Invooked when first time data is loading """
        # 1. input validation for better usage
        assert data is not None and fields is not None, "Please provide data and fields"
        # 2. Initiate DataFrameManager
        data_frame_ref = MultiResourceDataFrameManager()
        master_data = data_frame_ref.buildData(data=data, fields=fields)[1]
        # 3. Syncing master, slave, modified caches
        self.set(self.cache_key_master, master_data)
        self.set(self.cache_key_slave, master_data)
        # 4. Setting active cache_key
        self._set_active_cache_key(self.cache_key_slave)

    def set_search_params(
            self,
            data
    ):
        """ This is used to set the search params """
        self.set(self.cache_key_criteria, data)
        return True

    def get_search_params(
            self
    ):
        """ This is used to get the search params """
        return self.get(self.cache_key_criteria)

    def search_cache(
            self,
            **filters
    ):
        """ Used to filter over slave and return from the slave """
        # 1. Read the slave_data
        slave_data = self.get(self.cache_key_slave)
        # 2. filter the slave_data with filter attributes and sync it to the filtered cache
        filtered_data = slave_data
        for key, val in filters.items():
            filtered_data = filtered_data[([key] == val)]
        # 3. syncing filtereData with the result
        self.set(self.cache_key_filtered, filtered_data)
        # 4. Setting active cache key as filtered_keye
        self._set_active_cache_key(cache_key_filtered)
        # 5. Returning the filtered_data
        return self.get(self.cache_key_filtered)

    def refresh_cache(
            self
    ):
        """ This is used to reset the cache state to initial """
        # 1. Get the Queryset from Cache
        qset = self.get(self.cache_key_queryset)
        self.set_grid_cache_data(data=qset)

    def sort_cache(
            self,
            column,
            asc
    ):
        """ Used to sort the active cache(filtered/slave) """
        # 1. Sorting the data frame based on column
        sorted_data = self.get(self._get_active_cache_key()).sort(
            columns=[column], ascending=asc).reset_index(drop=True)
        # 2. Making active cachekey as sorted cache key
        self._set_active_cache_key(self.cache_key_sorted)
        # 3. syncing sorted_data with cache_key_filtered
        self.set(self.cache_key_sorted, sorted_data)
        # 4. Returning active Data(now it is sorted data)
        return self.get_data()

    def get_data(
            self
    ):
        """ Used to retrieve the data from the cache based on unikKey + self.cache_key"""
        # Returning the data from the active cache key
        active_data = self._get_active_cache_data()
        return active_data.to_dict(orient='records')

    def get_data_as_csv(
            self
    ):
        """ Used to return dataframe as csv """
        active_data = self._get_active_cache_data()
        return active_data.to_csv()

    def get_data_as_xls(
            self
    ):
        """ Used to return data as xls """
        sio = StringIO.StringIO()
        pandas_writer = pd.ExcelWriter(sio, general_exceptionngine='xlsxwriter')
        active_data = self._get_active_cache_data()
        # Create excel file here manually by serializing the fields
        active_data.to_excel(pandas_writer, sheet_name="download")
        pandas_writer.save()
        sio.seek(0)
        workbook = sio.getvalue()
        return workbook
