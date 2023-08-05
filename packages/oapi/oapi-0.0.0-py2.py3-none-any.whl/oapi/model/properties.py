import typing
from base64 import b64decode, b64encode
from collections import Mapping, Sequence, OrderedDict, MutableSequence, Set, Container
from copy import copy
from numbers import Real

import functools

from oapi import model


class Property(object):

    json_types = ('array', 'object', 'integer', 'number', 'string', 'boolean')  # type: typing.Sequence[str]
    formats = None  # type: Optional[typing.Sequence[str]]

    def __init__(
        self,
        types=None,  # type: typing.Sequence[Union[type, Property]]
        key=None,  # type: Optional[str]
        required=False,  # type: bool
        versions=None,  # type: Optional[typing.Collection]
    ):
        if isinstance(types, (type, Property)):
            types = (types,)
        else:
            types = copy(types)
        self.types = types  # type: Optional[Sequence[type]]
        self.key = key
        self.required = required
        if versions is not None:
            if isinstance(versions, str):
                versions = (versions,)
            else:
                versions = copy(versions)
        self.versions = versions  # type: Optional[typing.Collection]

    def load(self, data):
        # type: (typing.Any) -> typing.Any
        return data if self.types is None else polymorph(data, self.types)

    def dump(self, data):
        # type: (typing.Any) -> typing.Any
        return model.dump(data)


class String(Property):

    json_types = ('string',)  # type: Optional[typing.Sequence[str]]
    formats = (None,)  # type: Optional[typing.Sequence[str]]

    def __init__(
        self,
        key=None,  # type: Optional[str]
        required=False,  # type: bool
        versions=None,  # type: Optional[typing.Collection]
    ):
        super().__init__(
            types=(str,),
            key=key,
            required=required,
            versions=versions
        )


class Bytes(Property):

    json_types = ('string',)  # type: Optional[typing.Sequence[str]]
    formats = ('byte', )  # type: Optional[typing.Sequence[str]]

    def __init__(
        self,
        key=None,  # type: Optional[str]
        required=False,  # type: bool
        versions=None,  # type: Optional[typing.Collection]
    ):
        super().__init__(
            types=(bytes, bytearray),
            key=key,
            required=required,
            versions=versions
        )

    def load(self, data):
        # type: (str) -> bytes
        return b64decode(data)

    def dump(self, data):
        # type: (bytes) -> str
        return b64encode(data)


class Enum(Property):

    def __init__(
        self,
        types=None,  # type: Optional[Sequence[Union[type, Property]]]
        values=None,  # type: Optional[typing.Sequence]
        key=None,  # type: Optional[str]
        required=False,  # type: bool
        versions=None,  # type: Optional[typing.Collection]
    ):
        super().__init__(
            types=types,
            key=key,
            required=required,
            versions=versions
        )
        self.values = values  # type: Optional[typing.Sequence]

    @property
    def values(self):
        # type: () -> Optional[Tuple]
        return self._values

    @values.setter
    def values(self, values):
        # type: (Iterable) -> None
        if (values is not None) and (not isinstance(values, Sequence)):
            raise TypeError(
                '`values` must be a finite set or sequence, not `%s`.' %
                type(values).__name__
            )
        if values is not None:
            tuple(polymorph(v, self.types) for v in values)
        self._values = values

    def load(self, data):
        # type: (typing.Any) -> typing.Any
        if self.types is not None:
            data = polymorph(data, self.types)
        if (self.values is not None) and (data not in self.values):
            raise ValueError(
                'The value provided is not a valid option:\n%s\n\n' % repr(data) +
                'Valid options include:\n%s' % (
                    ','.join(repr(t) for t in self.value_types)
                )
            )
        return data


class Number(Property):

    json_types = ('number',)  # type: typing.Sequence[str]

    def __init__(
        self,
        key=None,  # type: Optional[str]
        required=False,  # type: bool
        versions=None,  # type: Optional[typing.Collection]
    ):
        # type: (...) -> None
        super().__init__(
            types=(Real,),
            key=key,
            required=required,
            versions=versions
        )


class Integer(Property):

    json_types = ('integer',)  # type: Optional[typing.Sequence[str]]

    def __init__(
        self,
        key=None,  # type: Optional[str]
        required=False,  # type: bool
        versions=None,  # type: Optional[typing.Collection]
    ):
        super().__init__(
            types=(int,),
            key=key,
            required=required,
            versions=versions
        )

    def load(self, data):
        # type: (typing.Any) -> typing.Any
        return int(data)

    def dump(self, data):
        # type: (typing.Any) -> typing.Any
        return int(data)


class Boolean(Property):

    json_types = ('boolean',)  # type: typing.Sequence[str]

    def __init__(
        self,
        key=None,  # type: Optional[str]
        required=False,  # type: bool
        versions=None,  # type: Optional[typing.Collection]
    ):
        # type: (...) -> None
        super().__init__(
            types=(bool,),
            key=key,
            required=required,
            versions=versions
        )

    def load(self, data):
        # type: (typing.Any) -> typing.Any
        return bool(data)

    def dump(self, data):
        # type: (typing.Any) -> typing.Any
        return bool(data)


class Array(Property):

    json_types = ('array',)  # type: typing.Sequence[str]

    def __init__(
        self,
        key=None,  # type: Optional[str]
        item_types=None,  # type: Optional[Union[type, typing.Sequence[Union[type, Property]]]]
        required=False,  # type: bool
        versions=None,  # type: Optional[typing.Collection]
    ):
        super().__init__(types=(Sequence,), key=key, required=required, versions=versions)
        if isinstance(item_types, (type, Property)):
            item_types = (item_types,)
        self.item_types = item_types  # type: Optional[typing.Sequence[Union[type, Property]]]

    def load(self, data):
        # type: (typing.Any) -> typing.Any
        return [polymorph(d, self.item_types) for d in data]


def polymorph(data, types):
    # type: (Any, typing.Sequence[Union[type, Property]]) -> type
    if types is None:
        return data
    closest_match = None
    data_keys = None
    for t in types:
        if (
            closest_match is None
        ) and isinstance(
            t,
            Property
        ) and (
            (
                t.types is None
            ) or isinstance(
                data,
                tuple(tt for tt in t.types if isinstance(tt, type))
            )
        ):
            data = t.load(data)
            break
        elif isinstance(t, type) and issubclass(t, model.Object) and isinstance(data, Mapping):
            data_keys = data_keys or set(data.keys())
            type_keys = {
                (v.key or k)
                for k, v in model.get_properties(t).items()
            }
            if not (data_keys - type_keys):
                unused = type_keys - data_keys
                if (
                    (closest_match is None) or
                    len(unused) < len(closest_match[-1])
                ):
                    closest_match = (t, unused)
    if closest_match is not None:
        data = closest_match[0](data)
    return data


class Object(Property):

    json_types = ('object',)  # type: typing.Sequence[str]

    def __init__(
        self,
        types=None,  # type: Optional[Union[type, Sequence[Union[type, Property]]]]
        value_types=None,  # type: Optional[Union[type, Sequence[Union[type, Property]]]]
        key=None,  # type: Optional[str]
        required=False,  # type: bool
        versions=None,  # type: Optional[typing.Collection]
    ):
        super().__init__(types=types, key=key, required=required, versions=versions)
        if value_types is not None:
            if isinstance(value_types, (type, Property)):
                value_types = (value_types,)
        self.value_types = value_types

    def load(self, data):
        # type: (typing.Mapping[str, Any]) -> typing.Mapping[str, Any]
        data = super().load(data)
        if isinstance(data, model.Object):
            return data
        else:
            if not isinstance(data, Mapping):
                raise TypeError(
                    'Data must be a mapping, not a `%s`.' % type(data).__name__
                )
            mapping = OrderedDict()
            for k, v in data.items():
                mapping[k] = polymorph(v, self.value_types)
            return mapping