from collections import Iterable
import numpy as np
from abc import ABCMeta, abstractmethod
from six import with_metaclass
import six
from .utils import docval, getargs, popargs

def __get_shape_helper(data):
    shape = list()
    if hasattr(data, '__len__'):
        shape.append(len(data))
        if len(data) and not isinstance(data[0], str):
            shape.extend(__get_shape_helper(data[0]))
    return tuple(shape)

def get_shape(data):
    if hasattr(data, '__len__') and not isinstance(data, str):
        return __get_shape_helper(data)
    else:
        return None

def get_type(data):
    if isinstance(data, str):
        return str
    if not hasattr(data, '__len__'):
        return type(data)
    else:
        if len(data) == 0:
            raise ValueError('cannot determine type for empty data')
        return get_type(data[0])

class AbstractDataChunkIterator(with_metaclass(ABCMeta, object)):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def recommended_chunk_shape(self):
        pass

    @abstractmethod
    def recommended_data_shape(self):
        pass

class DataChunkIterator(AbstractDataChunkIterator):
    """Custom iterator class used to iterate over chunks of data.

    Derived classes must ensure that self.shape and self.dtype are set properly.
    define the self.max_shape property describing the maximum shape of the array.
    In addition, derived classes must implement the __next__ method (or overwrite _read_next_chunk
    if the default behavior of __next__ should be reused). The __next__ method must return
    in each iteration 1) a numpy array with the data values for the chunk and 2) a numpy-compliant index tuple
    describing where the chunk is located within the complete data.  HINT: `numpy.s_ <https://docs.scipy.org/doc/numpy/reference/generated/numpy.s_.html>`_ provides a
    convenient way to generate index tuples using standard array slicing. There are
    a number of additional functions that one can overwrite to customize behavior, e.g,
    the :py:func:`~form.utils.DataChunkIterator.recommended_chunk_shape` or :py:func:`~form.utils.DataChunkIterator.recommended_data_shape`

    The default implementation accepts any iterable and assumes that we iterate over
    the first dimension of the data array. The default implemention supports buffered read,
    i.e., multiple values from the input iterator can be combined to a single chunk. This is
    useful for buffered I/O operations, e.g., to improve performance by accumulating data
    in memory and writing larger blocks at once.
    """
    @docval({'name': 'data', 'type': None, 'doc': 'The data object used for iteration', 'default': None},
            {'name': 'max_shape', 'type': tuple,
             'doc': 'The maximum shape of the full data array. Use None to indicate unlimited dimensions',
             'default': None},
            {'name': 'dtype', 'type': np.dtype, 'doc': 'The Numpy data type for the array', 'default': None},
            {'name': 'buffer_size', 'type': int, 'doc': 'Number of values to be buffered in a chunk', 'default': 1},
            )
    def __init__(self, **kwargs):
        """Initalize the DataChunkIterator"""
        # Get the user parameters
        self.data, self.max_shape, self.dtype, self.buffer_size = getargs('data',
                                                                          'max_shape',
                                                                          'dtype',
                                                                          'buffer_size',
                                                                          kwargs)
        # Create an iterator for the data if possible
        self.__data_iter = iter(self.data) if isinstance(self.data, Iterable) else None
        self.__next_chunk = DataChunk(None, None)
        self.__first_chunk_shape = None
        # Determine the shape of the data if possible
        if self.max_shape is None:
            # If the self.data object identifies it shape then use it
            if hasattr(self.data,  "shape"):
                self.max_shape = self.data.shape
                # Avoid the special case of scalar values by making them into a 1D numpy array
                if len(self.max_shape) == 0:
                    self.data = np.asarray([self.data, ])
                    self.max_shape = self.data.shape
                    self.__data_iter = iter(self.data)
            # Try to get an accurate idea of max_shape for other Python datastructures if possible.
            # Don't just callget_shape for a generator as that would potentially trigger loading of all the data
            elif isinstance(self.data, list) or isinstance(self.data, tuple):
                self.max_shape = ShapeValidator.get_data_shape(self.data, strict_no_data_load=True)

        # If we have a data iterator, then read the first chunk
        if self.__data_iter is not None: # and(self.max_shape is None or self.dtype is None):
            self._read_next_chunk()

        # If we still don't know the shape then try to determine the shape from the first chunk
        if self.max_shape is None and self.__next_chunk.data is not None:
            data_shape = ShapeValidator.get_data_shape(self.__next_chunk.data)
            self.max_shape = list(data_shape)
            try:
                self.max_shape[0] = len(self.data)  # We use self.data here because self.__data_iter does not allow len
            except TypeError:
                self.max_shape[0] = None
            self.max_shape = tuple(self.max_shape)

        # Determine the type of the data if possible
        if self.__next_chunk.data is not None:
            self.dtype = self.__next_chunk.data.dtype
            self.__first_chunk_shape = ShapeValidator.get_data_shape(self.__next_chunk.data)

    def __iter__(self):
        """Return the iterator object"""
        return self

    def _read_next_chunk(self):
        """Read a single chunk from self.__data_iter and store the results in
           self.__next_chunk

        :returns: self.__next_chunk, i.e., the DataChunk object describing the next chunk
        """
        if self.__data_iter is not None:
            curr_next_chunk = []
            for i in range(self.buffer_size):
                try:
                    curr_next_chunk.append(next(self.__data_iter))
                except StopIteration:
                    pass
            next_chunk_size = len(curr_next_chunk)
            if next_chunk_size == 0:
                self.__next_chunk = DataChunk(None, None)
            else:
                self.__next_chunk.data = np.asarray(curr_next_chunk)
                if self.__next_chunk.selection is None:
                    self.__next_chunk.selection = slice(0, next_chunk_size)
                else:
                    self.__next_chunk.selection = slice(self.__next_chunk.selection.stop,
                                                        self.__next_chunk.selection.stop+next_chunk_size)
        else:
            self.__next_chunk = DataChunk(None, None)

        return self.__next_chunk

    def __next__(self):
        """Return the next data chunk or raise a StopIteration exception if all chunks have been retrieved.

        HINT: numpy.s_ provides a convenient way to generate index tuples using standard array slicing. This
        is often useful to define the DataChunkk.selection of the current chunk

        :returns: DataChunk object with the data and selection of the current chunk
        :rtype: DataChunk

        """
        # If we have not already read the next chunk, then read it now
        if self.__next_chunk.data is None:
            self._read_next_chunk()
        # If we do not have any next chunk
        if self.__next_chunk.data is None:
            raise StopIteration
        # If this is the first time we see a chunk then remember the size of the first chunk
        if self.__first_chunk_shape is None:
            self.__first_chunk_shape = self.__next_chunk.data.shape
        # Keep the next chunk we need to return
        curr_chunk = DataChunk(self.__next_chunk.data,
                               self.__next_chunk.selection)
        # Remove the data for the next chunk from our list since we are returning it here.
        # This is to allow the GarbageCollector to remmove the data when it goes out of scope and avoid
        # having 2 full chunks in memory if not necessary
        self.__next_chunk.data = None
        # Return the current next chunk
        return curr_chunk

    next = __next__

    @docval(returns='Tuple with the recommended chunk shape or None if no particular shape is recommended.')
    def recommended_chunk_shape(self):
        """Recommend a chunk shape.

        To optimize iterative write the chunk should be aligned with the common shape of chunks returned by __next__
        or if those chunks are too large, then a well-aligned subset of those chunks. This may also be
        any other value in case one wants to recommend chunk shapes to optimize read rather
        than write. The default implementation returns None, indicating no preferential chunking option."""
        return None

    @docval(returns='Recommended initial shape for the full data. This should be the shape of the full dataset' +
                    'if known beforehand or alternatively the minimum shape of the dataset. Return None if no ' +
                    'recommendation is available')
    def recommended_data_shape(self):
        """Recommend an initial shape of the data. This is useful when progressively writing data and
        we want to recommend and initial size for the dataset"""
        if self.max_shape is not None:
            if np.all([i is not None for i in self.max_shape]):
                return self.max_shape
        return self.__first_chunk_shape


class DataChunk(object):
    """
    Class used to describe a data chunk. Used in DataChunkIterator to describe

    :ivar data: Numpy ndarray with the data value(s) of the chunk
    :ivar selection: Numpy index tuple describing the location of the chunk
    """
    @docval({'name': 'data', 'type': np.ndarray, 'doc': 'Numpy array with the data value(s) of the chunk', 'default': None},
            {'name':'selection', 'type': None, 'doc': 'Numpy index tuple describing the location of the chunk', 'default': None})
    def __init__(self, **kwargs):
        self.data, self.selection = getargs('data', 'selection', kwargs)

    def __len__(self):
        if self.data is not None:
            return len(self.data)
        else:
            return 0

class ShapeValidator(object):
    """
    Helper class used to compare dimensions.

    This class consists mainly of a set of static helper functions used to check
    that the shape of arrays is compliant.
    """

    def __init__(self):
        """The typical use of this class is by calling static methods that return instances of ShapeValidatorResult"""
        pass

    @staticmethod
    def get_data_shape(data, strict_no_data_load=False):
        """
        Helper function used to determine the shape of the given array.

        :param data: Array for which we should determine the shape.
        :type data: List, numpy.ndarray, DataChunkIterator, any object that support __len__ or .shape.
        :param strict_no_data_load: In order to determin the shape of nested tuples and lists, this function
                    recursively inspects elements along the dimensions, assuming that the data has a regular,
                    rectangular shape. In the case of out-of-core iterators this means that the first item
                    along each dimensions would potentially be loaded into memory. By setting this option
                    we enforce that this does not happen, at the cost that we may not be able to determine
                    the shape of the array.
        :return: Tuple of ints indicating the size of known dimensions. Dimenions for which the size is unknown
                 will be set to None.
        """
        def __get_shape_helper(local_data):
            shape = list()
            if hasattr(local_data, '__len__'):
                shape.append(len(local_data))
                if len(local_data) and not isinstance(local_data[0], str):
                    shape.extend(__get_shape_helper(local_data[0]))
            return tuple(shape)
        if isinstance(data, DataChunkIterator):
            return data.max_shape
        if hasattr(data, 'shape'):
            return data.shape
        if hasattr(data, '__len__') and not isinstance(data, str):
            if not strict_no_data_load or (isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set)):
                return __get_shape_helper(data)
            else:
                return None
        else:
            return None

    @staticmethod
    def assertEqualShape(data1,
                         data2,
                         axes1=None,
                         axes2=None,
                         name1=None,
                         name2=None,
                         ignore_undetermined=True):
        """
        Ensure that the shape of data1 and data2 match along the given dimensions

        :param data1: The first input array
        :type data1: List, Tuple, np.ndarray, DataChunkIterator etc.
        :param data2: The second input array
        :type data2: List, Tuple, np.ndarray, DataChunkIterator etc.
        :param name1: Optional string with the name of data1
        :param name2: Optional string with the name of data2
        :param axes1: The dimensions of data1 that should be matched to the dimensions of data2. Set to None to
                      compare all axes in order.
        :type axes1: int, Tuple of ints, List of ints, or None
        :param axes2: The dimensions of data2 that should be matched to the dimensions of data1. Must have
                      the same length as axes1. Set to None to compare all axes in order.
        :type axes1: int, Tuple of ints, List of ints, or None
        :param ignore_undetermined: Boolean indicating whether non-matching unlimited dimensions should be ignored,
                   i.e., if two dimension don't match because we can't determine the shape of either one, then
                   should we ignore that case or treat it as no match

        :return: Bool indicating whether the check passed and a string with a message about the matching process
        """
        # Create the base return object
        response = ShapeValidatorResult()
        # Determine the shape of the datasets
        response.shape1 = ShapeValidator.get_data_shape(data1)
        response.shape2 = ShapeValidator.get_data_shape(data2)
        # Determine the number of dimensions of the datasets
        num_dims_1 = len(response.shape1) if response.shape1 is not None else None
        num_dims_2 = len(response.shape2) if response.shape2 is not None else None
        # Determine the string names of the datasets
        n1 = name1 if name1 is not None else ("data1 at " + str(hex(id(data1))))
        n2 = name2 if name2 is not None else ("data2 at " + str(hex(id(data2))))
        # Determine the axes we should compare
        response.axes1 = list(range(num_dims_1)) if axes1 is None else ([axes1] if isinstance(axes1, int) else axes1)
        response.axes2 = list(range(num_dims_2)) if axes2 is None else ([axes2] if isinstance(axes2, int) else axes2)
        # Validate the array shape
        # 1) Check the number of dimensions of the arrays
        if (response.axes1 is None and response.axes2 is None) and num_dims_1 != num_dims_2:
            response.result = False
            response.error = 'NUM_DIMS_ERROR'
            response.message =response.SHAPE_ERROR[response.error]
            response.message += " %s is %sD and %s is %sD" %(n1, num_dims_1, n2, num_dims_2)
        # 2) Check that we have the same number of dimensions to compare on both arrays
        elif len(response.axes1) != len(response.axes2):
            response.result = False
            response.error = 'NUM_AXES_ERROR'
            response.message = response.SHAPE_ERROR[response.error]
            response.message += " Cannot compare axes %s with %s" % (str(response.axes1), str(response.axes2))
        # 3) Check that the datasets have sufficient numner of dimensions
        elif np.max(response.axes1) >= num_dims_1 or np.max(response.axes2) >= num_dims_2:
            response.result = False
            response.error = 'AXIS_OUT_OF_BOUNDS'
            response.message = response.SHAPE_ERROR[response.error]
            if np.max(response.axes1) >= num_dims_1:
                response.message += "Insufficient number of dimensions for %s -- Expected %i found %i" % \
                                    (n1, np.max(response.axes1)+1, num_dims_1)
            elif np.max(response.axes2) >= num_dims_2:
                response.message += "Insufficient number of dimensions for %s -- Expected %i found %i" % \
                                    (n2, np.max(response.axes2)+1, num_dims_2)
        # 4) Compare the lenght of the dimensions we should validate
        else:
            unmatched = []
            ignored = []
            for ax in zip(response.axes1, response.axes2):
                if response.shape1[ax[0]] != response.shape2[ax[1]]:
                    if ignore_undetermined and (response.shape1[ax[0]] is None or response.shape2[ax[1]] is None):
                        ignored.append(ax)
                    else:
                        unmatched.append(ax)
            response.unmatched = unmatched
            response.ignored = ignored

            # Check if everyting checked out
            if len(response.unmatched) == 0:
                response.result = True
                response.error = None
                response.message = response.SHAPE_ERROR[response.error]
                if len(response.ignored) > 0:
                    response.message += " Ignored undetermined axes %s" % str(response.ignored)
            else:
                response.result = False
                response.error = 'AXIS_LEN_ERROR'
                response.message = response.SHAPE_ERROR[response.error]
                response.message += "Axes %s with size %s of %s did not match dimensions %s with sizes %s of %s." % \
                                    (str([un[0] for un in response.unmatched]),
                                     str([response.shape1[un[0]] for un in response.unmatched]),
                                     n1,
                                     str([un[1] for un in response.unmatched]),
                                     str([response.shape2[un[1]] for un in response.unmatched]),
                                     n2)
                if len(response.ignored) > 0:
                    response.message += " Ignored undetermined axes %s" % str(response.ignored)
        return response


class ShapeValidatorResult(object):
    """Class for storing results from validating the shape of multi-dimensional arrays.

    This class is used to store results generated by ShapeValidator

    :ivar result: Boolean indicating whether results matched or not
    :type result: bool
    :ivar message: Message indicating the result of the matching procedure
    :type messaage: str, None
    """
    SHAPE_ERROR = {None: 'All required axes matched',
                   'NUM_DIMS_ERROR': 'Unequal number of dimensions.',
                   'NUM_AXES_ERROR': "Unequal number of axes for comparison.",
                   'AXIS_OUT_OF_BOUNDS': "Axis index for comparison out of bounds.",
                   'AXIS_LEN_ERROR': "Unequal length of axes."}
    """
    Dict where the Keys are the type of errors that may have occured during shape comparison and the
    values are strings with default error messages for the type.
    """

    @docval({'name': 'result', 'type': bool, 'doc': 'Result of the shape validation', 'default': False},
            {'name': 'message', 'type': str, 'doc': 'Message describing the result of the shape validation', 'default': None},
            {'name': 'ignored', 'type': tuple, 'doc': 'Axes that have been ignored in the validaton process', 'default': tuple(), 'ndim': 1},
            {'name': 'unmatched', 'type': tuple, 'doc': 'List of axes that did not match during shape validation', 'default': tuple(), 'ndim': 1},
            {'name': 'error', 'type': str, 'doc': 'Error that may have occurred. One of ERROR_TYPE', 'default': None},
            {'name': 'shape1', 'type': tuple, 'doc': 'Shape of the first array for comparison', 'default': tuple(), 'ndim': 1},
            {'name': 'shape2', 'type': tuple, 'doc': 'Shape of the second array for comparison', 'default': tuple(), 'ndim': 1},
            {'name': 'axes1', 'type': tuple, 'doc': 'Axes for the first array that should match', 'default': tuple(), 'ndim': 1},
            {'name': 'axes2', 'type': tuple, 'doc': 'Axes for the second array that should match', 'default': tuple(), 'ndim': 1},
            )
    def __init__(self, **kwargs):
        self.result, self.message, self.ignored, self.unmatched, self.error, self.shape1, self.shape2, self.axes1, self.axes2 = \
            getargs('result', 'message', 'ignored', 'unmatched', 'error', 'shape1', 'shape2', 'axes1', 'axes2', kwargs)

    def __setattr__(self, key, value):
        """
        Overwrite to ensure that, e.g., error_message is not set to an illegal value.
        """
        if key == 'error':
            if value not in self.SHAPE_ERROR.keys():
                raise ValueError("Illegal error type. Error must be one of ShapeValidatorResult.SHAPE_ERROR: %s" % str(self.SHAPE_ERROR))
            else:
                super(ShapeValidatorResult, self).__setattr__(key, value)
        elif key in ['shape1', 'shape2', 'axes1', 'axes2', 'ignored', 'unmatched']: # Make sure we sore tuples
            super(ShapeValidatorResult, self).__setattr__(key, tuple(value))
        else:
            super(ShapeValidatorResult, self).__setattr__(key, value)

    def __getattr__(self, item):
         """
         Overwrite to allow dynamic retrival of the default message
         """
         if item == 'default_message':
             return self.SHAPE_ERROR[self.error]
         return self.__getattribute__(item)
