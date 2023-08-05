import numpy as np
import copy as _copy
import itertools as _itertools
import posixpath as _posixpath
from abc import ABCMeta

from form.utils import docval, getargs

class Builder(dict, metaclass=ABCMeta):

    @docval({'name': 'name', 'type': str, 'doc': 'the name of the group'},
            {'name': 'parent', 'type': 'Builder', 'doc': 'the parent builder of this Builder', 'default': None},
            {'name': 'source', 'type': str, 'doc': 'the source of the data in this builder e.g. file name', 'default': None})
    def __init__(self, **kwargs):
        name, parent, source = getargs('name', 'parent', 'source', kwargs)
        super().__init__()
        self.__name = name
        self.__parent = parent
        if source is not None:
            self.__source = source
        elif parent is not None:
            self.__source = parent.source
        else:
            self.__source = None

    @property
    def name(self):
        ''' The name of this Builder '''
        return self.__name

    @property
    def source(self):
        ''' The source of this Builder '''
        return self.__source

    @property
    def parent(self):
        ''' The parent Builder of this Builder '''
        return self.__parent

    @parent.setter
    def parent(self, p):
        if self.__parent is None:
            self.__parent = p
        else:
            raise ValueError('Cannot reset parent once it is specified')

class BaseBuilder(Builder):
    __attribute = 'attributes'

    @docval({'name': 'name', 'type': str, 'doc': 'the name of the group'},
            {'name': 'attributes', 'type': dict, 'doc': 'a dictionary of attributes to create in this group',
             'default': dict()},
            {'name': 'parent', 'type': 'GroupBuilder', 'doc': 'the parent builder of this Builder', 'default': None},
            {'name': 'source', 'type': str, 'doc': 'the source of the data represented in this Builder', 'default': None})
    def __init__(self, **kwargs):
        name, attributes, parent, source = getargs('name', 'attributes', 'parent', 'source', kwargs)
        super(BaseBuilder, self).__init__(name, parent, source)
        super().__setitem__(BaseBuilder.__attribute, dict())
        for name, val in attributes.items():
            self.set_attribute(name, val)

    @property
    def attributes(self):
        ''' The attributes stored in this Builder object '''
        return super().__getitem__(BaseBuilder.__attribute)

    @docval({'name':'name', 'type': str, 'doc': 'the name of the attribute'},
            {'name':'value', 'type': None, 'doc': 'the attribute value'})
    def set_attribute(self, **kwargs):
        ''' Set an attribute for this group. '''
        name, value = getargs('name', 'value', kwargs)
        super().__getitem__(BaseBuilder.__attribute)[name] = value
        #self.obj_type[name] = BaseBuilder.__attribute

    @docval({'name': 'builder', 'type': 'BaseBuilder', 'doc': 'the BaseBuilder to merge attributes from '})
    def deep_update(self, **kwargs):
        ''' Merge attributes from the given BaseBuilder into this builder '''
        builder = kwargs['builder']
        # merge attributes
        for name, value in super(GroupBuilder, builder).__getitem__(BaseBuilder.__attribute).items():
            self.set_attribute(name, value)

class GroupBuilder(BaseBuilder):
    __link = 'links'
    __group = 'groups'
    __dataset = 'datasets'
    __attribute = 'attributes'

    @docval({'name': 'name', 'type': str, 'doc': 'the name of the group'},
            {'name': 'groups', 'type': dict, 'doc': 'a dictionary of subgroups to create in this group',
             'default': dict()},
            {'name': 'datasets', 'type': dict, 'doc': 'a dictionary of datasets to create in this group',
             'default': dict()},
            {'name': 'attributes', 'type': dict, 'doc': 'a dictionary of attributes to create in this group',
             'default': dict()},
            {'name': 'links', 'type': dict, 'doc': 'a dictionary of links to create in this group',
             'default': dict()},
            {'name': 'parent', 'type': 'GroupBuilder', 'doc': 'the parent builder of this Builder', 'default': None},
            {'name': 'source', 'type': str, 'doc': 'the source of the data represented in this Builder', 'default': None})
    def __init__(self, **kwargs):
        '''
        Create a GroupBuilder object
        '''
        name, groups, datasets, links, attributes, parent, source = getargs('name', 'groups', 'datasets', 'links', 'attributes', 'parent', 'source', kwargs)
        self.obj_type = dict()
        super(GroupBuilder, self).__init__(name, attributes, parent, source)
        super().__setitem__(GroupBuilder.__group, dict())
        super().__setitem__(GroupBuilder.__dataset, dict())
        super().__setitem__(GroupBuilder.__link, dict())
        self.__name = name
        for name, group in groups.items():
            self.set_group(group)
        for name, dataset in datasets.items():
            self.set_dataset(dataset)
        for name, link in links.items():
            self.set_link(link)

    @property
    def groups(self):
        ''' The subgroups contained in this GroupBuilder '''
        return super().__getitem__(GroupBuilder.__group)

    @property
    def datasets(self):
        ''' The datasets contained in this GroupBuilder '''
        return super().__getitem__(GroupBuilder.__dataset)

    @property
    def links(self):
        ''' The datasets contained in this GroupBuilder '''
        return super().__getitem__(GroupBuilder.__link)

    @docval({'name':'name', 'type': str, 'doc': 'the name of the attribute'},
            {'name':'value', 'type': None, 'doc': 'the attribute value'})
    def set_attribute(self, **kwargs):
        ''' Set an attribute for this group '''
        name, value = getargs('name', 'value', kwargs)
        super(GroupBuilder, self).set_attribute(name, value)
        self.obj_type[name] = GroupBuilder.__attribute

    def __set_builder(self, builder, obj_type):
        name = builder.name
        if name in self.obj_type:
            if self.obj_type[name] != obj_type:
                raise KeyError("'%s' already exists as %s" % (name, self.obj_type[name]))
        super().__getitem__(obj_type)[name] = builder
        self.obj_type[name] = obj_type
        if builder.parent is None:
            #setattr(builder, '_%s__parent' % builder.__class__.__name__, self)
            builder.parent = self

    @docval({'name':'name', 'type': str, 'doc': 'the name of this dataset'},
            {'name':'data', 'type': None, 'doc': 'a dictionary of datasets to create in this dataset', 'default': None},
            {'name':'dtype', 'type': (type, np.dtype), 'doc': 'the datatype of this dataset', 'default': None},
            {'name':'attributes', 'type': dict, 'doc': 'a dictionary of attributes to create in this dataset', 'default': dict()},
            {'name':'maxshape', 'type': (int, tuple), 'doc': 'the shape of this dataset. Use None for scalars', 'default': None},
            {'name':'chunks', 'type': bool, 'doc': 'whether or not to chunk this dataset', 'default': False},
            returns='the DatasetBuilder object for the dataset', rtype='DatasetBuilder')
    def add_dataset(self, **kwargs):
        ''' Create a dataset and add it to this group '''
        name = kwargs.pop('name')
        builder = DatasetBuilder(name, self, **kwargs)
        self.set_dataset(builder)
        return builder

    @docval({'name': 'builder', 'type': 'DatasetBuilder', 'doc': 'the DatasetBuilder that represents this dataset'})
    def set_dataset(self, **kwargs):
        ''' Add a dataset to this group '''
        builder = getargs('builder', kwargs)
        self.__set_builder(builder, GroupBuilder.__dataset)

    @docval({'name': 'name', 'type': str, 'doc': 'the name of this subgroup'},
            {'name': 'groups', 'type': dict, 'doc': 'a dictionary of subgroups to create in this subgroup', 'default': dict()},
            {'name': 'datasets', 'type': dict, 'doc': 'a dictionary of datasets to create in this subgroup', 'default': dict()},
            {'name': 'attributes', 'type': dict, 'doc': 'a dictionary of attributes to create in this subgroup', 'default': dict()},
            {'name': 'links', 'type': dict, 'doc': 'a dictionary of links to create in this subgroup', 'default': dict()},
            returns='the GroupBuilder object for the subgroup', rtype='GroupBuilder')
    def add_group(self, **kwargs):
        ''' Add a subgroup with the given data to this group '''
        name = kwargs.pop('name')
        builder = GroupBuilder(name, parent=self, **kwargs)
        self.set_group(builder)
        return builder

    @docval({'name': 'builder', 'type': 'GroupBuilder', 'doc': 'the GroupBuilder that represents this subgroup'})
    def set_group(self, **kwargs):
        ''' Add a subgroup to this group '''
        name, builder, = getargs('name', 'builder', kwargs)
        self.__set_builder(builder, GroupBuilder.__group)

    @docval({'name': 'name', 'type': str, 'doc': 'the name of this link'},
            {'name': 'target', 'type': ('GroupBuilder', 'DatasetBuilder'), 'doc': 'the target Builder'},
            returns='the builder object for the soft link', rtype='LinkBuilder')
    def add_link(self, **kwargs):
        ''' Create a soft link and add it to this group '''
        name, target = getargs('name', 'target', kwargs)
        builder = LinkBuilder(name, target, self)
        self.set_link(builder)
        return builder

    @docval({'name':'builder', 'type': 'LinkBuilder', 'doc': 'the LinkBuilder that represents this link'})
    def set_link(self, **kwargs):
        ''' Add a link to this group '''
        builder = getargs('builder', kwargs)
        self.__set_builder(builder, GroupBuilder.__link)

    #TODO: write unittests for this method
    def deep_update(self, builder):
        ''' Recursively update subgroups in this group '''
        super(GroupBuilder, self).deep_update(builder)
        # merge subgroups
        groups = super(GroupBuilder, builder).__getitem__(GroupBuilder.__group)
        self_groups = super().__getitem__(GroupBuilder.__group)
        for name, subgroup in groups.items():
            if name in self_groups:
                self_groups[name].deep_update(subgroup)
            else:
                self.set_group(subgroup)
        # merge datasets
        datasets = super(GroupBuilder, builder).__getitem__(GroupBuilder.__dataset)
        self_datasets = super().__getitem__(GroupBuilder.__dataset)
        for name, dataset in datasets.items():
            #self.add_dataset(name, dataset)
            if name in self_datasets:
                self_datasets[name].deep_update(dataset)
                #super().__getitem__(GroupBuilder.__dataset)[name] = dataset
            else:
                self.set_dataset(dataset)
        # merge links
        for name, link in super(GroupBuilder, builder).__getitem__(GroupBuilder.__link).items():
            self.set_link(link)

    def is_empty(self):
        '''Returns true if there are no datasets, attributes, links or
           subgroups that contain datasets, attributes or links. False otherwise.
        '''
        if (len(super().__getitem__(GroupBuilder.__dataset)) or
            len(super().__getitem__(GroupBuilder.__attribute)) or
            len(super().__getitem__(GroupBuilder.__link))):
            return False
        elif len(super().__getitem__(GroupBuilder.__group)):
            return all(g.is_empty() for g in super().__getitem__(GroupBuilder.__group).values())
        else:
            return True

    def __getitem__(self, key):
        '''Like dict.__getitem__, but looks in groups,
           datasets, attributes, and links sub-dictionaries.
        '''
        try:
            key_ar = _posixpath.normpath(key).split('/')
            return self.__get_rec(key_ar)
        except KeyError:
            raise KeyError(key)

    def get(self, key, default=None):
        '''Like dict.get, but looks in groups,
           datasets, attributes, and links sub-dictionaries.
        '''
        try:
            key_ar = _posixpath.normpath(key).split('/')
            return self.__get_rec(key_ar)
        except KeyError:
            return default

    def __get_rec(self, key_ar):
        # recursive helper for __getitem__
        if len(key_ar) == 1:
            return super().__getitem__(self.obj_type[key_ar[0]])[key_ar[0]]
        else:
            if key_ar[0] in super().__getitem__(GroupBuilder.__group):
                return super().__getitem__(GroupBuilder.__group)[key_ar[0]].__get_rec(key_ar[1:])
        raise KeyError(key_ar[0])


    def __setitem__(self, args, val):
        raise NotImplementedError('__setitem__')

    def __contains__(self, item):
        return self.obj_type.__contains__(item)

    def items(self):
        '''Like dict.items, but iterates over key-value pairs in groups,
           datasets, attributes, and links sub-dictionaries.
        '''
        return _itertools.chain(super().__getitem__(GroupBuilder.__group).items(),
                                super().__getitem__(GroupBuilder.__dataset).items(),
                                super().__getitem__(GroupBuilder.__attribute).items(),
                                super().__getitem__(GroupBuilder.__link).items())

    def keys(self):
        '''Like dict.keys, but iterates over keys in groups, datasets,
           attributes, and links sub-dictionaries.
        '''
        return _itertools.chain(super().__getitem__(GroupBuilder.__group).keys(),
                                super().__getitem__(GroupBuilder.__dataset).keys(),
                                super().__getitem__(GroupBuilder.__attribute).keys(),
                                super().__getitem__(GroupBuilder.__link).keys())

    def values(self):
        '''Like dict.values, but iterates over values in groups, datasets,
           attributes, and links sub-dictionaries.
        '''
        return _itertools.chain(super().__getitem__(GroupBuilder.__group).values(),
                                super().__getitem__(GroupBuilder.__dataset).values(),
                                super().__getitem__(GroupBuilder.__attribute).values(),
                                super().__getitem__(GroupBuilder.__link).values())

class DatasetBuilder(BaseBuilder):
    @docval({'name': 'name', 'type': str, 'doc': 'the name of the dataset'},
            {'name': 'data', 'type': None, 'doc': 'a dictionary of datasets to create in this dataset', 'default': None},
            {'name': 'dtype', 'type': (type, np.dtype), 'doc': 'the datatype of this dataset', 'default': None},
            {'name': 'attributes', 'type': dict, 'doc': 'a dictionary of attributes to create in this dataset', 'default': dict()},
            {'name': 'maxshape', 'type': (int, tuple), 'doc': 'the shape of this dataset. Use None for scalars', 'default': None},
            {'name': 'chunks', 'type': bool, 'doc': 'whether or not to chunk this dataset', 'default': False},
            {'name': 'parent', 'type': GroupBuilder, 'doc': 'the parent builder of this Builder', 'default': None},
            {'name': 'source', 'type': str, 'doc': 'the source of the data in this builder', 'default': None})
    def __init__(self, **kwargs):
        ''' Create a Builder object for a dataset '''
        name, data, dtype, attributes, maxshape, chunks, parent, source = getargs('name', 'data', 'dtype', 'attributes', 'maxshape', 'chunks', 'parent', 'source', kwargs)
        super(DatasetBuilder, self).__init__(name, attributes, parent, source)
        self['data'] = data
        self['attributes'] = _copy.deepcopy(attributes)
        self.__chunks = chunks
        self.__maxshape = maxshape
        self.__dtype = dtype
        self.__name = name

    @property
    def data(self):
        ''' The data stored in the dataset represented by this builder '''
        return self['data']

    def chunks(self):
        ''' Whether or not this dataset is chunked '''
        return self.__chunks

    def maxshape(self):
        ''' The max shape of this object '''
        return self.__maxshape

    def dtype(self):
        ''' The data type of this object '''
        return self.__dtype

    @docval({'name':'dataset', 'type': 'DatasetBuilder', 'doc': 'the DatasetBuilder to merge into this DatasetBuilder'})
    def deep_update(self, **kwargs):
        '''Merge data and attributes from given DatasetBuilder into this DatasetBuilder'''
        dataset = getargs('dataset', kwargs)
        if dataset.data:
            self['data'] = dataset.data #TODO: figure out if we want to add a check for overwrite
        self['attributes'].update(dataset.attributes)

class LinkBuilder(Builder):

    @docval({'name': 'name', 'type': str, 'doc': 'the name of the dataset'},
            {'name': 'builder', 'type': (DatasetBuilder, GroupBuilder), 'doc': 'the target of this link'},
            {'name': 'parent', 'type': GroupBuilder, 'doc': 'the parent builder of this Builder', 'default': None},
            {'name': 'source', 'type': str, 'doc': 'the source of the data in this builder', 'default': None})
    def __init__(self, **kwargs):
        name, builder, parent, source = getargs('name', 'builder', 'parent', 'source', kwargs)
        super().__init__(name, parent, source)
        self['builder'] = builder

    @property
    def builder(self):
        ''' The target builder object '''
        return self['builder']

