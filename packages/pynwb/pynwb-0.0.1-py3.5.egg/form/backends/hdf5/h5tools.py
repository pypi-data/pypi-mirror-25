from collections import Iterable
import numpy as np
import os.path
from h5py import File, Group, Dataset, special_dtype, SoftLink, ExternalLink

from form.utils import DataChunkIterator, docval, getargs, popargs

from ..io import FORMIO
from form.build import GroupBuilder, DatasetBuilder, LinkBuilder, BuildManager

class HDF5IO(FORMIO):

    @docval({'name': 'path', 'type': str, 'doc': 'the  path to the HDF5 file to write to'},
            {'name': 'manager', 'type': BuildManager, 'doc': 'the BuildManager to use for I/O'})
    def __init__(self, **kwargs):
        path, manager = popargs('path', 'manager', kwargs)
        super(HDF5IO, self).__init__(manager)
        self.__path = path
        self.__built = dict()

    @docval(returns='a GroupBuilder representing the NWB Dataset', rtype='GroupBuilder')
    def read_builder(self):
        self.open()
        #f = File(self.__path, 'r+')
        f_builder = self.__read_group(self.__file, 'root')
        return f_builder

    def __set_built(self, fpath, path, builder):
        self.__built.setdefault(fpath, dict()).setdefault(path, builder)

    def __get_built(self, fpath, path):
        fdict = self.__built.get(fpath)
        if fdict:
            return fdict.get(path)
        else:
            return None

    def __read_group(self, h5obj, name=None):
        kwargs = {
            "attributes": dict(h5obj.attrs.items()),
            "groups": dict(),
            "datasets": dict(),
            "links": dict()
        }
        if name is None:
            name = os.path.basename(h5obj.name)
        for k in h5obj:
            sub_h5obj = h5obj.get(k)
            link_type = h5obj.get(k, getlink=True)
            if isinstance(link_type, SoftLink) or isinstance(link_type, ExternalLink):
                # get path of link (the key used for tracking what's been built)
                target_path = link_type.path
                builder_name = os.path.basename(target_path)
                # get builder if already read, else build it
                builder = self.__get_built(sub_h5obj.file.filename, target_path)
                if builder is None:
                    # NOTE: all links must have absolute paths
                    if isinstance(sub_h5obj, Dataset):
                        builder = self.__read_dataset(sub_h5obj, builder_name)
                    else:
                        builder = self.__read_group(sub_h5obj, builder_name)
                    self.__set_built(sub_h5obj.file.filename, target_path, builder)
                kwargs['links'][builder_name] = LinkBuilder(builder)
            else:
                builder = self.__get_built(sub_h5obj.file.filename, sub_h5obj.name)
                obj_type = None
                read_method = None
                if isinstance(sub_h5obj, Dataset):
                    read_method = self.__read_dataset
                    obj_type = kwargs['datasets']
                else:
                    read_method = self.__read_group
                    obj_type = kwargs['groups']
                if builder is None:
                    builder = read_method(sub_h5obj)
                    self.__set_built(sub_h5obj.file.filename, sub_h5obj.name, builder)
                obj_type[builder.name] = builder
        ret = GroupBuilder(name, **kwargs)
        return ret

    def __read_dataset(self, h5obj, name=None):
        kwargs = {
            "attributes": dict(h5obj.attrs.items()),
            "data": h5obj,
            "dtype": h5obj.dtype,
            "maxshape": h5obj.maxshape
        }
        if name is None:
            name = os.path.basename(h5obj.name)
        ret = DatasetBuilder(name, **kwargs)
        return ret

    def open(self):
        open_flag = 'w'
        if os.path.exists(self.__path):
            open_flag = 'r+'
        self.__file = File(self.__path, open_flag)

    def close(self):
        self.__file.close()

    @docval({'name': 'builder', 'type': GroupBuilder, 'doc': 'the GroupBuilder object representing the NWBFile'})
    def write_builder(self, **kwargs):
        f_builder = getargs('builder', kwargs)
        self.open()
        for name, gbldr in f_builder.groups.items():
            write_group(self.__file, name, gbldr.groups, gbldr.datasets, gbldr.attributes, gbldr.links)
        for name, dbldr in f_builder.datasets.items():
            write_dataset(self.__file, name, dbldr.data, dbldr.attributes)
        set_attributes(self.__file, f_builder.attributes)


@docval({'name': 'obj', 'type': (Group, Dataset), 'doc': 'the HDF5 object to add attributes to'},
        {'name': 'attributes', 'type': dict, 'doc': 'a dict containing the attributes on the Group, indexed by attribute name'},
        is_method=False)
def set_attributes(**kwargs):
    obj, attributes = getargs('obj', 'attributes', kwargs)
    for key, value in attributes.items():
        if any(isinstance(value, t) for t in (set, list, tuple)):
            tmp = tuple(value)
            if len(tmp) > 0:
                if isinstance(tmp[0], str):
                    max_len = max(len(s) for s in tmp)
                    dt = '|S%d' % max_len
                    value = np.array(tmp, dtype=dt)
                value = np.array(value)
        obj.attrs[key] = value

@docval({'name': 'parent', 'type': Group, 'doc': 'the parent HDF5 object'},
        {'name': 'name', 'type': str, 'doc': 'the name of the Dataset to write'},
        {'name': 'subgroups', 'type': dict, 'doc': 'a dict containing GroupBuilders for subgroups in this group, indexed by group name'},
        {'name': 'datasets', 'type': dict, 'doc': 'a dict containing DatasetBuilders for datasets in this group, indexed by dataset name'},
        {'name': 'attributes', 'type': dict, 'doc': 'a dict containing the attributes on the Group, indexed by attribute name'},
        {'name': 'links', 'type': dict, 'doc': 'a dict containing LinkBuilders for links in this group, indexed by link name'},
        returns='the Group that was created', rtype='Group', is_method=False)
def write_group(**kwargs):
    parent, name, subgroups, datasets, attributes, links = getargs('parent', 'name', 'subgroups', 'datasets', 'attributes', 'links', kwargs)
    group = parent.require_group(name)
    # write all groups
    if subgroups:
        for subgroup_name, builder in subgroups.items():
            # do not create an empty group without attributes or links
            tmp_links = write_group(group,
                            subgroup_name,
                            builder.groups,
                            builder.datasets,
                            builder.attributes,
                            builder.links)
    # write all datasets
    if datasets:
        for dset_name, builder in datasets.items():
            write_dataset(group,
                          dset_name,
                          builder.get('data'),
                          builder.get('attributes'))
    # write all links
    if links:
        for link_name, builder in links.items():
            write_link(group, name, builder.target)
    set_attributes(group, attributes)
    return group

@docval({'name': 'parent', 'type': Group, 'doc': 'the parent HDF5 object'},
        {'name': 'name', 'type': str, 'doc': 'the name of the Link to write'},
        {'name': 'target_builder', 'type': (DatasetBuilder, GroupBuilder), 'doc': 'the Builder representing the target'},
        returns='the Link that was created', rtype='Link', is_method=False)
def write_link(**kwargs):
    parent, name, target_builder = getargs('parent', 'name', 'target_builder', kwargs)
    # get target path
    names = list()
    curr = target_builder
    while curr is not None:
        names.append(curr.name)
        curr = target_builder.parent
    delim = "/"
    path = "%s%s" % (delim, delim.join(reversed(names)))
    # source will indicate target_builder's location
    if parent.file.filename == target_builder.source:
        link_obj = SoftLink(path)
    else:
        link_obj = ExternalLink(target_builder.source, path)
    parent[name] = link_obj
    return link_obj

def __get_shape_helper(data):
    shape = list()
    if hasattr(data, '__len__'):
        shape.append(len(data))
        if len(data) and not isinstance(data[0], str):
            shape.extend(__get_shape_helper(data[0]))
    return tuple(shape)

def __get_shape(data):
    if hasattr(data, '__len__') and not isinstance(data, str):
        return __get_shape_helper(data)
    else:
        return None

def __get_type(data):
    if isinstance(data, str):
        return special_dtype(vlen=bytes)
    elif not hasattr(data, '__len__'):
        return type(data)
    else:
        return __get_type(data[0])

def isinstance_inmemory_array(data):
    """Check if an object is a common in-memory data structure"""
    return isinstance(data, list) or \
           isinstance(data, np.ndarray) or \
           isinstance(data, tuple) or \
           isinstance(data, set) or \
           isinstance(data, str) or \
           isinstance(data, frozenset)

__data_types = (
    str,
    DataChunkIterator,
    float,
    int,
    Iterable
)

@docval({'name': 'parent', 'type': Group, 'doc': 'the parent HDF5 object'},
        {'name': 'name', 'type': str, 'doc': 'the name of the Dataset to write'},
        {'name': 'data', 'type': __data_types, 'doc': 'the data object to be written'},
        {'name': 'attributes', 'type': dict, 'doc': 'a dict containing the attributes on the Dataset, indexed by attribute name'},
        returns='the Dataset that was created', rtype=Dataset, is_method=False)
def write_dataset(**kwargs):
    """ Write a dataset to HDF5

    The function uses other dataset-dependent write functions, e.g,
    __scalar_fill__, __list_fill__ and __chunked_iter_fill__ to write the data.
    """
    parent, name, data, attributes = getargs('parent', 'name', 'data', 'attributes', kwargs)
    dset = None
    if isinstance(data, str):
        dset = __scalar_fill__(parent, name, data)
    elif isinstance(data, DataChunkIterator):
        dset = __chunked_iter_fill__(parent, name, data)
    elif isinstance(data, Iterable) and not isinstance_inmemory_array(data):
        dset = __chunked_iter_fill__(parent, name, DataChunkIterator(data=data, buffer_size=100))
    elif hasattr(data, '__len__'):
        dset = __list_fill__(parent, name, data)
    else:
        dset = __scalar_fill__(parent, name, data)
    set_attributes(dset, attributes)
    return dset

def __selection_max_bounds__(selection):
    """Determine the bounds of a numpy selection index tuple"""
    if isinstance(selection, int):
        return selection+1
    elif isinstance(selection, slice):
        return selection.stop
    elif isinstance(selection, list) or isinstance(selection, np.ndarray):
        return np.nonzero(selection)[0][-1]+1
    elif isinstance(selection, tuple):
        return tuple([__selection_max_bounds__(i) for i in selection])

def __scalar_fill__(parent, name, data):
    dtype = __get_type(data)
    dset = parent.require_dataset(name, data=data, shape=None, dtype=dtype)
    return dset

def __chunked_iter_fill__(parent, name, data):
    """
    Write data to a dataset one-chunk-at-a-time based on the given DataChunkIterator

    :param parent: The parent object to which the dataset should be added
    :type parent: h5py.Group, h5py.File
    :param name: The name of the dataset
    :type name: str
    :param data: The data to be written.
    :type data: DataChunkIterator

    """
    recommended_chunks = data.recommended_chunk_shape()
    chunks = True if recommended_chunks is None else recommended_chunks
    baseshape = data.recommended_data_shape()
    dset = parent.require_dataset(name, shape=baseshape, dtype=data.dtype, maxshape=data.max_shape, chunks=chunks)
    for chunk_i in data:
        # Determine the minimum array dimensions to fit the chunk selection
        max_bounds = __selection_max_bounds__(chunk_i.selection)
        if not hasattr(max_bounds, '__len__'):
            max_bounds = (max_bounds,)
        # Determine if we need to expand any of the data dimensions
        expand_dims = [i for i, v in enumerate(max_bounds) if v is not None and v > dset.shape[i]]
        # Expand the dataset if needed
        if len(expand_dims) > 0:
            new_shape = np.asarray(dset.shape)
            new_shape[expand_dims] = np.asarray(max_bounds)[expand_dims]
            dset.resize(new_shape)
        # Process and write the data
        dset[chunk_i.selection] = chunk_i.data
    return dset

def __list_fill__(parent, name, data):
    data_shape = __get_shape(data)
    data_dtype = __get_type(data)
    dset = parent.require_dataset(name, shape=data_shape, dtype=data_dtype)
    if len(data) > dset.shape[0]:
        new_shape = list(dset.shape)
        new_shape[0] = len(data)
        dset.resize(new_shape)
    dset[:] = data
    return dset
