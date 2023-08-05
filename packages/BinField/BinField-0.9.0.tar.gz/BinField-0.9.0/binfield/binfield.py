#    Copyright 2016 - 2017 Alexey Stepanov aka penguinolog
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

# cython: binding=True, embedsignature=True

"""BinField module.

Implements BinField in Python
"""

from __future__ import unicode_literals

import collections
import copy
import math

import six

__all__ = ('BinField', )


string_types = (
    str if six.PY3
    else six.text_type, six.binary_type
)


def _is_descriptor(obj):
    """Return True if obj is a descriptor, False otherwise."""
    return (
        hasattr(obj, '__get__') or
        hasattr(obj, '__set__') or
        hasattr(obj, '__delete__')
    )


def _is_dunder(name):
    """Return True if a __dunder__ name, False otherwise."""
    return (name[:2] == name[-2:] == '__' and
            name[2:3] != '_' and
            name[-3:-2] != '_' and
            len(name) > 4)


def _is_sunder(name):
    """Return True if a _sunder_ name, False otherwise."""
    return (name[0] == name[-1] == '_' and
            name[1:2] != '_' and
            name[-2:-1] != '_' and
            len(name) > 2)


def _is_valid_slice(obj):
    """Slice is valid for BinField operations.

    :type obj: slice
    :rtype: bool
    """
    valid_precondition = isinstance(obj, slice) and obj.step is None
    if not valid_precondition:
        return False
    if obj.start is not None and obj.stop is not None:
        return valid_precondition and 0 <= obj.start < obj.stop
    return valid_precondition


def _is_valid_slice_mapping(obj):
    """Object is valid slice mapping.

    :rtype: bool
    """
    return (
        isinstance(obj, (tuple, list)) and len(obj) == 2 and
        isinstance(obj[0], int) and isinstance(obj[1], int) and
        0 <= obj[0] < obj[1]
    )


def _mapping_filter(item):
    """Filter for naming records from namespace.

    :param item: namespace item
    :type item: tuple
    :rtype: bool
    """
    name, obj = item

    if not isinstance(name, string_types):
        return False

    if name in {'_index_'}:
        return True

    # Descriptors, special methods, protected
    if _is_descriptor(obj) or _is_dunder(name) or name.startswith('_'):
        return False

    # Index / slice / slice from iterable
    if isinstance(
        obj, int
    ) or _is_valid_slice(
        obj
    ) or _is_valid_slice_mapping(
        obj
    ):
        return True

    # Not nested
    if not isinstance(obj, dict):
        return False

    # Process nested
    return all((_mapping_filter(value) for value in obj.items()))


def _get_index(val):
    """Extract real index from index."""
    if isinstance(val, int) or _is_valid_slice(val):
        return val
    if _is_valid_slice_mapping(val):
        return slice(*val)
    if isinstance(val, dict):
        return slice(*val['_index_'])


def _get_mask(start, end):
    """Make default mask.

    :type start: int
    :type end:  int
    :rtype: int
    """
    return (1 << end) - (1 << start)


def _get_start_index(src):
    """Internal method for sorting mapping.

    :param src: tuple from dict.items()
    :type src: tuple
    :rtype: int
    """
    if isinstance(src[1], int):
        return src[1]
    return _get_index(src[1]).start


def _prepare_mapping(mapping):
    """Check indexes for intersections.

    :type mapping: dict
    :rtype: collections.OrderedDict
    """
    mapping_mask = 0
    new_mapping = collections.OrderedDict()
    cycle_end = False

    # pylint: disable=undefined-loop-variable
    def check_update_mapping_mask(mask):
        """Check mask for validity and return updated value.

        :type mask: int
        :rtype: int
        """
        if mapping_mask & mask != 0:
            raise IndexError(
                'Mapping key {key} has intersection with other keys '
                'by mask {mask:b}'.format(
                    key=m_key,
                    mask=mapping_mask & mask
                ))
        return mapping_mask | mask

    # pylint: enable=undefined-loop-variable

    if '_index_' in mapping:
        new_mapping['_index_'] = mapping.pop('_index_')

    unexpected = [
        item for item in mapping.items() if not _mapping_filter(item)
    ]

    if unexpected:
        raise ValueError(
            'Mapping contains unexpected data: '
            '{!r}'.format(unexpected))

    for m_key, m_val in sorted(
        mapping.items(),
        key=_get_start_index
    ):
        if cycle_end:
            raise IndexError(
                'Mapping after non-ending slice index! '
                'First key: {}'.format(m_key))

        if isinstance(m_val, (list, tuple)):
            new_mapping[m_key] = slice(*m_val)  # Mapped slice -> slice
            mapping_mask = check_update_mapping_mask(_get_mask(*m_val))
        elif isinstance(m_val, int):
            mapping_mask = check_update_mapping_mask(
                _get_mask(m_val, m_val + 1)
            )
            new_mapping[m_key] = m_val
        elif isinstance(m_val, dict):  # nested mapping
            mapping_mask = check_update_mapping_mask(
                _get_mask(*m_val['_index_'])
            )
            new_mapping[m_key] = _prepare_mapping(m_val)
        else:
            if m_val.stop:
                mapping_mask = check_update_mapping_mask(
                    _get_mask(
                        m_val.start if m_val.start else 0,
                        m_val.stop
                    )
                )
            else:
                if mapping_mask & (1 << m_val.start) != 0:
                    raise IndexError(
                        'Mapping key {key} has intersection '
                        'with other keys by mask {mask:b}'.format(
                            key=m_key,
                            mask=mapping_mask & (1 << m_val.start)
                        ))
                cycle_end = True
            new_mapping[m_key] = m_val

    return new_mapping


def _make_mapping_property(key):
    """Property generator. Fixing lazy calculation.

    :rtype: property
    """
    return property(
        fget=lambda self: self.__getitem__(key),
        fset=lambda self, val: self.__setitem__(key, val),
        doc="""mapping key: {}""".format(key)
    )


def _make_static_ro_property(name, val):
    """Property generator for static cases.

    :type name: str
    :type val: object
    """
    return property(
        fget=lambda _=None: val,
        doc="""Read-only {}""".format(name)
    )


def _py2_str(src):
    """Convert text to correct python type."""
    if not six.PY3 and isinstance(src, six.text_type):
        return src.encode(
            encoding='utf-8',
            errors='strict',
        )
    return src


class BaseBinFieldMeta(object):
    """Fake class for BinFieldMeta compilation and class instance creation."""

    pass


class BinField(object):
    """Fake class for BinFieldMeta compilation."""

    pass


class BaseMeta(type):
    """Metaclass for BaseClass creation."""

    @property
    def _value_(cls):
        """Internal value (integer)."""
        return NotImplemented

    @property
    def _size_(cls):
        """Only for sized (Not BaseClass)."""
        return NotImplemented

    @property
    def _bit_size_(cls):
        """Only for sized (Not BaseClass)."""
        return NotImplemented

    @property
    def _mask_(cls):
        """Only if mask presents (Not BaseClass)."""
        return NotImplemented

    @property
    def _mapping_(cls):
        """Only for indexed (Not BaseClass)."""
        return NotImplemented


class BinFieldMeta(BaseMeta, type):
    """Metaclass for BinField class and subclasses construction."""

    # noinspection PyInitNewSignature
    def __new__(mcs, name, bases, classdict):
        """BinField metaclass.

        :type name: str
        :type bases: tuple
        :type classdict: dict
        :returns: new class
        """
        name = _py2_str(name)

        if not (
            BaseBinFieldMeta in bases or
            any((issubclass(base, BaseBinFieldMeta) for base in bases))
        ):
            # Top level baseclass: cleanup
            for key in ('_value_', '_size_', '_mask_', '_mapping_'):
                classdict.pop(key, None)  # pragma: no cover
            return super(
                BinFieldMeta,
                mcs
            ).__new__(mcs, name, bases, classdict)

        meta_dict = {}
        meta_name = _py2_str("{}Meta".format(name))

        if '_index_' in classdict:
            raise ValueError(
                '_index_ is reserved index for slicing nested BinFields'
            )

        size = classdict.pop('_size_', None)
        mask_from_size = None

        if size is not None:
            if not isinstance(size, int):
                raise TypeError(
                    'Pre-defined size has invalid type: {!r}'.format(size)
                )

            if size <= 0:
                raise ValueError('Size must be positive value !')

            mask_from_size = (1 << size) - 1

        mask = classdict.pop('_mask_', mask_from_size)

        if mask is not None:
            if not isinstance(mask, six.integer_types):
                raise TypeError(
                    'Pre-defined mask has invalid type: {!r}'.format(mask)
                )
            if mask < 0:
                raise ValueError('BitMask is strictly positive!')

            if size is None:
                # noinspection PyUnresolvedReferences
                size = mask.bit_length()

        meta_dict['_size_'] = classdict['_size_'] = \
            _make_static_ro_property('size', size)

        meta_dict['_mask_'] = classdict['_mask_'] = \
            _make_static_ro_property('mask', mask)

        mapping = classdict.pop('_mapping_', None)

        if mapping is None:
            mapping = {}

            for m_key, m_val in filter(
                    _mapping_filter,
                    classdict.copy().items()
            ):
                if isinstance(m_val, (list, tuple)):
                    mapping[m_key] = slice(*m_val)  # Mapped slice -> slice
                else:
                    mapping[m_key] = m_val
                del classdict[m_key]

        garbage = {
            name: obj for name, obj in classdict.items()
            if not (
                _is_dunder(name) or _is_sunder(name) or _is_descriptor(obj)
            )
        }

        if garbage:
            raise TypeError(
                'Several data is not recognized in class structure: '
                '{!r}'.format(garbage)
            )

        ready_mapping = _prepare_mapping(mapping)

        if ready_mapping:
            meta_dict['_mapping_'] = classdict['_mapping_'] = \
                _make_static_ro_property('mapping',
                                         copy.deepcopy(ready_mapping)
                                         )

            for m_key in ready_mapping:
                classdict[_py2_str(m_key)] = _make_mapping_property(m_key)
                meta_dict[_py2_str(m_key)] = _make_static_ro_property(
                    m_key,
                    _get_index(ready_mapping[m_key])
                )

        else:
            meta_dict['_mapping_'] = classdict['_mapping_'] = \
                _make_static_ro_property('mapping', None)

        classdict['_cache_'] = {}  # Use for subclasses memorize

        if BinField not in bases:
            return super(
                BinFieldMeta,
                mcs
            ).__new__(
                mcs, name, bases, classdict)

        # noinspection PyPep8Naming
        RealMeta = type(
            meta_name,
            (type,),
            meta_dict
        )

        # pylint: disable=bad-mcs-classmethod-argument
        class SubMeta(RealMeta, BinFieldMeta, type):
            """Mixin metaclass for creating BinField subclasses.

            Properties is made in RealMeta and here we are creating new class
            by the single possible way (usage of super() is impossible).
            """

            # noinspection PyMethodParameters,PyInitNewSignature
            def __new__(smcs, sname, sbases, sns):
                for base in sbases:
                    if base is not BinField and issubclass(base, BinField):
                        raise TypeError("Cannot extend BinField")

                sns['__slots__'] = ()  # No any new fields on instances

                return type.__new__(SubMeta, sname, sbases, sns)

        # pylint: enable=bad-mcs-classmethod-argument

        return type.__new__(SubMeta, name, bases, classdict)

    @classmethod
    def makecls(mcs, name, mapping=None, mask=None, size=None):
        """Create new BinField subclass.

        :param name: Class name
        :type name: str
        :param mapping: Data mapping
        :type mapping: dict
        :param mask: Data mask for new class
        :type mask: int
        :param size: BinField bit length
        :type size: int
        :returns: BinField subclass
        """
        classdict = {
            '_size_': size,
            '_mask_': mask,
            '__slots__': ()
        }
        if mapping is not None:
            classdict['_mapping_'] = mapping
        # noinspection PyTypeChecker
        return mcs.__new__(mcs, name, (BinField, ), classdict)


# noinspection PyRedeclaration
BaseBinFieldMeta = type.__new__(  # noqa
    BinFieldMeta,
    _py2_str('BaseBinFieldMeta'),
    (object, ),
    {'__slots__': ()}
)


# noinspection PyRedeclaration,PyMissingConstructor
class BinField(BaseBinFieldMeta):  # noqa  # redefinition of unused 'BinField'
    """BinField representation."""

    __slots__ = ['__value', '__parent_link']

    _cache_ = {}  # Will be replaced by the same by metaclass, but helps lint

    _size_ = None
    _mask_ = None
    _mapping_ = None

    # pylint: disable=super-init-not-called
    def __init__(self, x=0, base=10, _parent=None):
        """Create new BinField object from integer value.

        :param x: Start value
        :type x: typing.Union[int, str, bytes]
        :param base: base for start value
        :type base: int
        :param _parent: Parent link. For internal usage only.
        :type _parent: typing.Optional[typing.Tuple[BinField, slice]]
        """
        self.__value = (
            x if isinstance(x, six.integer_types)
            else int(x, base=base)
        )
        if self._mask_:
            self.__value &= self._mask_
        self.__parent_link = _parent

    # pylint: enable=super-init-not-called

    @property
    def _bit_size_(self):
        """Number of bits necessary to represent self in binary.

        Could be frozen by constructor
        :rtype: int
        """
        return self._size_ if self._size_ else self._value_.bit_length()

    def __len__(self):
        """Data length in bytes."""
        length = int(math.ceil(self._bit_size_ / 8.))
        return length if length != 0 else 1

    @property
    def _value_(self):
        """Internal value (integer).

        :rtype: int
        """
        if self.__parent_link is not None:  # Update value from parent
            obj, offset = self.__parent_link
            self.__value = (obj & (self._mask_ << offset)) >> offset
        return self.__value

    # noinspection PyProtectedMember
    @_value_.setter
    def _value_(self, new_value):
        """Internal value (integer).

        :type new_value: int
        """
        if self._mask_:
            new_value &= self._mask_

        if self.__parent_link is not None:
            obj, offset = self.__parent_link

            obj[:] =\
                int(obj) & ~(self._mask_ << offset) | (new_value << offset)

        self.__value = new_value

    # integer methods
    def __int__(self):
        """Conversion to normal int.

        :rtype: int
        """
        return self._value_

    def __index__(self):
        """Special method used for bin()/hex/oct/slicing support.

        :rtype: int
        """
        return self._value_

    # math operators
    def __abs__(self):
        """int mimic.

        :rtype: int
        """
        return self._value_

    def __gt__(self, other):
        """Comparing logic.

        :rtype: bool
        """
        return self._value_ > int(other)

    def __ge__(self, other):
        """Comparing logic.

        :rtype: bool
        """
        return self._value_ >= int(other)

    def __lt__(self, other):
        """Comparing logic.

        :rtype: bool
        """
        return self._value_ < int(other)

    def __le__(self, other):
        """Comparing logic.

        :rtype: bool
        """
        return self._value_ <= int(other)

    # pylint: disable=protected-access
    def __eq__(self, other):
        """Comparing logic.

        :rtype: bool
        """
        # As integer
        if isinstance(other, (int, self.__class__)):
            return self._value_ == other
        if isinstance(other, BinField):
            # noinspection PyUnresolvedReferences,PyProtectedMember
            return (
                self._value_ == other._value_ and
                self._mapping_ == other._mapping_ and
                len(self) == len(other)
            )
        return False
    # pylint: enable=protected-access

    def __ne__(self, other):
        """Comparing logic.

        :rtype: bool
        """
        return not self == other

    # Modify Bitwise operations
    def __iand__(self, other):
        """int mimic."""
        self._value_ &= int(other)
        return self

    def __ior__(self, other):
        """int mimic."""
        self._value_ |= int(other)
        return self

    def __ixor__(self, other):
        """int mimic."""
        self._value_ ^= int(other)
        return self

    # Non modify operations: new BinField will re-use _mapping_
    # pylint: disable=no-value-for-parameter
    def __and__(self, other):
        """int mimic.

        :rtype: BinField
        """
        return self.__class__(self._value_ & int(other))

    def __or__(self, other):
        """int mimic.

        :rtype: BinField
        """
        return self.__class__(self._value_ | int(other))

    def __xor__(self, other):
        """int mimic.

        :rtype: BinField
        """
        return self.__class__(self._value_ ^ int(other))
    # pylint: enable=no-value-for-parameter

    # Integer modify operations
    def __iadd__(self, other):
        """int mimic."""
        res = self._value_ + int(other)
        if self._size_ and self._size_ < res.bit_length():
            raise OverflowError(
                'Result value {} not fill in '
                'data length ({} bits)'.format(res, self._size_))
        if res < 0:
            raise ValueError(
                'BinField could not be negative!'
            )
        self._value_ = res
        return self

    def __isub__(self, other):
        """int mimic."""
        return self.__iadd__(-other)

    # Integer non-modify operations. New object is BinField, if not overflow
    # new BinField will re-use _mapping_
    # pylint: disable=no-value-for-parameter
    def __add__(self, other):
        """int mimic.

        :rtype: typing.Union[int, BinField]
        """
        res = self._value_ + int(other)
        if res < 0:
            raise ValueError(
                'BinField could not be negative! '
                'Value {} is bigger, than {}'.format(
                    other, self._value_
                )
            )
        if self._size_ and self._size_ < res.bit_length():
            return res
        return self.__class__(res)

    def __sub__(self, other):
        """int mimic.

        :rtype: typing.Union[int, BinField]
        """
        return self.__add__(-other)

    # pylint: enable=no-value-for-parameter

    # Integer -> integer operations
    def __mul__(self, other):
        """int mimic.

        :rtype: int
        """
        return self._value_ * other

    def __lshift__(self, other):
        """int mimic.

        :rtype: int
        """
        return self._value_ << other

    def __rshift__(self, other):
        """int mimic.

        :rtype: int
        """
        return self._value_ >> other

    def __bool__(self):
        """int mimic.

        :rtype: bool
        """
        return bool(self._value_)

    # Data manipulation: hash, pickle
    def __hash__(self):
        """Usage for indexes."""
        return hash((
            self.__class__,
            self._value_,
            # link is not included, but linked objects will have different
            # base classes due to on the fly generation
        ))

    # pylint: disable=no-value-for-parameter
    def __copy__(self):
        """Copy logic.

        :rtype: BinField

        .. note:: Uplink is destroyed on copy.
        """
        return self.__class__(self._value_)

    # pylint: enable=no-value-for-parameter

    def __getstate__(self):
        """Pickling.

        :rtype: typing.Dict[str: int]
        """
        if self.__parent_link:
            raise ValueError('Linked BinFields does not supports pickle')
        return {
            'x': self.__value,
        }

    def __getnewargs__(self):  # PYPY requires this
        """required for pickle.

        :rtype: typing.Tuple
        """
        return ()

    def __setstate__(self, state):
        """Restore from pickle.

        :type state: typing.Dict[str: int]
        """
        self.__init__(**state)  # getstate returns enough data for __init__

    def _get_child_cls_(self, mask, name, cls_mask, size, mapping=None):
        """Get child class with memorize support.

        :type mask: int
        :type name: str
        :type cls_mask: int
        :type size: int
        :type mapping: typing.Optional[
                           typing.Dict[
                               str,
                               typing.Union[slice, int, typing.Dict]
                           ]
                       ]
        """
        # Memorize
        # pylint: disable=protected-access
        if (mask, name) not in self.__class__._cache_:
            cls = BinFieldMeta.makecls(
                name=name,
                mapping=mapping,
                mask=cls_mask,
                size=size
            )
            self.__class__._cache_[(mask, name)] = cls
        cls = self.__class__._cache_[(mask, name)]
        # pylint: enable=protected-access
        return cls

    # Access as dict
    def _getslice_(self, item, mapping=None, name=None):
        """Get slice from self.

        :type item: slice
        :type mapping: typing.Optional[typing.Dict]
        :type name: typing.Optional[str]
        :rtype: BinField
        """
        if item.start is None and item.stop is None:
            return self.__copy__()

        if item.start:
            if self._size_ and item.start > self._size_:
                raise IndexError(
                    'Index {} is out of data length {}'
                    ''.format(item, self._size_))

        if name is None:
            name = '{cls}_slice_{start!s}_{stop!s}'.format(
                cls=self.__class__.__name__,
                start=item.start if item.start else 0,
                stop=item.stop
            )

        stop = (
            item.stop
            if item.stop and (not self._size_ or item.stop < self._size_)
            else self._bit_size_
        )

        start = item.start if item.start else 0

        mask = _get_mask(start, stop)

        if self._mask_ is not None:
            mask &= self._mask_

        cls_mask = mask >> start

        # Memorize
        cls = self._get_child_cls_(
            mask=mask,
            name=name,
            cls_mask=cls_mask,
            size=stop - start,
            mapping=mapping,
        )
        return cls((self._value_ & mask) >> start, _parent=(self, start))

    def __getitem__(self, item):
        """Extract bits.

        :type item: union(str, int, slice, tuple, list)
        :rtype: BinField
        :raises: IndexError
        """
        if isinstance(item, int):
            name = '{cls}_index_{index}'.format(
                cls=self.__class__.__name__,
                index=item
            )
            return self._getslice_(slice(item, item + 1), name=name)

        if _is_valid_slice(item):
            return self._getslice_(item)

        if _is_valid_slice_mapping(item):
            return self._getslice_(slice(*item))

        if not isinstance(item, string_types) or item.startswith('_'):
            raise IndexError(item)

        if self._mapping_ is None:
            raise IndexError("Mapping is not available")

        # pylint: disable=no-member
        idx = self._mapping_.get(item)
        # pylint: enable=no-member
        if isinstance(idx, int):
            return self._getslice_(slice(idx, idx + 1), name=item)
        if isinstance(idx, slice):
            return self._getslice_(idx, name=item)

        if isinstance(idx, dict):  # Nested _mapping_
            # Extract slice
            slc = slice(*idx['_index_'])
            # Build new _mapping_ dict
            mapping = copy.deepcopy(idx)
            del mapping['_index_']
            # Get new val
            return self._getslice_(slc, mapping=mapping, name=item)

        raise IndexError(item)

    def _setslice_(self, key, value):
        """Set value by slice.

        :type key: slice
        :type value: int
        """
        # Copy scenario
        if key.start is None and key.stop is None:
            if self._size_ and value.bit_length() > self._size_:
                raise OverflowError(
                    'Data value to set is bigger, than bitfield size: '
                    '{} > {}'.format(value.bit_length(), self._size_)
                )
            self._value_ = value
            return

        if self._size_ and key.stop and key.stop > self._size_:
            raise OverflowError(
                'Stop index is out of data length: '
                '{} > {}'.format(key.stop, self._size_)
            )

        stop = key.stop if key.stop else self._bit_size_
        start = key.start if key.start else 0

        if value.bit_length() > stop:
            raise ValueError('Data size is bigger, than slice')
        if key.start:
            if value.bit_length() > stop - start:
                raise ValueError('Data size is bigger, than slice')

        value <<= start  # Get correct binary position

        get_mask = _get_mask(start, stop)
        if self._mask_:
            get_mask &= self._mask_

        self._value_ = self._value_ & ~get_mask | value

    def __setitem__(self, key, value):
        """Indexed setter.

        :type key: union(str, int, slice, list, tuple)
        :type value: int
        """
        if not isinstance(value, int):
            raise TypeError(
                'BinField value could be set only as int'
            )

        if isinstance(key, int):
            return self._setslice_(slice(key, key + 1), value)

        if _is_valid_slice(key):
            return self._setslice_(key, value)

        if _is_valid_slice_mapping(key):
            return self._setslice_(slice(*key), value)

        if not isinstance(key, string_types):
            raise IndexError(key)

        if self._mapping_ is None:
            raise IndexError("Mapping is not available")

        # pylint: disable=no-member
        idx = self._mapping_.get(key)
        # pylint: enable=no-member
        if isinstance(idx, (int, slice)):
            return self.__setitem__(idx, value)

        if isinstance(
            idx, dict
        ) and _is_valid_slice_mapping(
            idx['_index_']
        ):  # Nested _mapping_
            # Extract slice from nested
            return self._setslice_(slice(*idx['_index_']), value)

        raise IndexError(key)

    # Representations
    def __pretty_str__(
        self,
        parser,
        indent,
        no_indent_start
    ):
        """real __str__ code."""
        indent = 0 if no_indent_start else indent
        indent_step = 2 if parser is None else parser.indent_step
        max_indent = 20 if parser is None else parser.max_indent
        py2_str = parser is None  # do not break str on py27

        formatter = _Formatter(
            max_indent=max_indent,
            indent_step=indent_step,
            py2_str=py2_str
        )
        return formatter(
            src=self,
            indent=indent
        )

    def __str__(self):
        """__str__ for usage in print."""
        # noinspection PyTypeChecker
        return self.__pretty_str__(None, 0, True)

    def __pretty_repr__(
        self,
        _,
        indent,
        no_indent_start
    ):
        """real __repr__ code."""
        indent = 0 if no_indent_start else indent
        if self.__parent_link:
            pre = '<'
            post = ' at 0x{:X}>'.format(id(self))
        else:
            pre = post = ''
        return (
            '{spc:<{indent}}{pre}{cls}(x=0x{x:0{len}X}, base=16){post}'.format(
                spc='',
                indent=indent,
                pre=pre,
                cls=self.__class__.__name__,
                x=self._value_,
                len=len(self) * 2,
                post=post
            )
        )

    def __repr__(self):
        """__repr__ for logging/debugging usage."""
        return self.__pretty_repr__(None, 0, True)

    def __dir__(self):
        """__dir__ wrapper (used as completion-helper)."""
        if self._mapping_ is not None:
            # pylint: disable=no-member
            keys = list(sorted(self._mapping_.keys()))
            # pylint: enable=no-member
        else:
            keys = []
        return (
            ['_bit_size_', '_mapping_', '_mask_', '_value_', '_size_'] + keys
        )


class _Formatter(object):
    def __init__(
        self,
        max_indent=20,
        indent_step=4,
        py2_str=False,

    ):
        """BinField dedicated str formatter.

        :param max_indent: maximal indent before classic repr() call
        :type max_indent: int
        :param indent_step: step for the next indentation level
        :type indent_step: int
        :param py2_str: use Python 2.x compatible strings instead of unicode
        :type py2_str: bool
        """
        self.__max_indent = max_indent
        self.__indent_step = indent_step
        self.__py2_str = py2_str and not six.PY3
        # Python 2 only behavior

    @property
    def indent_step(self):
        """Indent step getter.

        :rtype: int
        """
        return self.__indent_step

    def next_indent(self, indent, multiplier=1):
        """Next indentation value.

        :param indent: current indentation value
        :type indent: int
        :param multiplier: steps amount
        :type multiplier: int
        :rtype: int
        """
        return indent + multiplier * self.indent_step

    @property
    def max_indent(self):
        """Max indent getter.

        :rtype: int
        """
        return self.__max_indent

    def _str_bf_items(self, src, indent=0):
        """repr dict items.

        :param src: object to process
        :type src: dict
        :param indent: start indentation
        :type indent: int
        :rtype: generator
        """
        max_len = max([len(str(key)) for key in src]) if src else 0
        for key, val in src.items():
            yield "\n{spc:<{indent}}{key!s:{size}} = {val}".format(
                spc='',
                indent=self.next_indent(indent),
                size=max_len,
                key=key,
                val=self.process_element(
                    val,
                    indent=self.next_indent(indent, multiplier=2),
                    no_indent_start=True
                )
            )

    # pylint: disable=protected-access
    # noinspection PyUnresolvedReferences,PyProtectedMember
    def process_element(self, src, indent=0, no_indent_start=False):
        """Make human readable representation of object.

        :param src: object to process
        :type src: BinField
        :param indent: start indentation
        :type indent: int
        :param no_indent_start:
            do not indent open bracket and simple parameters
        :type no_indent_start: bool
        :return: formatted string
        :rtype: str
        """
        if src._mask_ is None:
            mask = ''
        else:
            mask = ' & 0b{:b}'.format(src._mask_)

        if src._mapping_ and indent < self.max_indent:
            as_dict = collections.OrderedDict(
                ((key, src[key]) for key in src._mapping_)
            )
            result = ''.join(self._str_bf_items(src=as_dict, indent=indent))

            return (
                "{nl}"
                "{spc:<{indent}}"
                "<{data} == "
                "0x{data:0{length}X} == "
                "(0b{data:0{bit_length}b}{mask})"
                "{result}\n"
                "{spc:<{indent}}>".format(
                    nl='\n' if no_indent_start else '',
                    spc='',
                    indent=indent,
                    data=src._value_,
                    length=len(src) * 2,
                    bit_length=src._bit_size_,
                    mask=mask,
                    result=result,
                )
            )

        indent = 0 if no_indent_start else indent
        return (
            '{spc:<{indent}}'
            '<{data} == 0x{data:0{length}X} == (0b{data:0{blength}b}{mask})>'
            ''.format(
                spc='',
                indent=indent,
                data=src._value_,
                length=len(src) * 2,
                blength=src._bit_size_,
                mask=mask
            )
        )
    # pylint: enable=protected-access

    def __call__(
        self,
        src,
        indent=0,
        no_indent_start=False
    ):
        """Make human readable representation of object.

        :param src: object to process
        :type src: union(binary_type, text_type, int, iterable, object)
        :param indent: start indentation
        :type indent: int
        :param no_indent_start:
            do not indent open bracket and simple parameters
        :type no_indent_start: bool
        :return: formatted string
        """
        result = self.process_element(
            src,
            indent=indent,
            no_indent_start=no_indent_start
        )
        if self.__py2_str:  # pragma: no cover
            return result.encode(
                encoding='utf-8',
                errors='backslashreplace',
            )
        return result
