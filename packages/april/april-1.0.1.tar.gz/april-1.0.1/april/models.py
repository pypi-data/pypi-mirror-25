# -*- coding: utf-8 -*-

import inspect

from .utils import is_nested_type


class ModelMeta(type):

    def __new__(cls, name, bases, attrs):
        _fields = dict()

        # get inherited fileds
        for base in bases:
            inherited_fields = base._fields if hasattr(base, '_fields') else []
            _fields.update(inherited_fields)

        # save fields metainfo in klass._fields
        class_attrs = {}
        for key, field_type in attrs.items():
            if inspect.isclass(field_type):
                _fields.update({key: field_type})
            else:
                class_attrs[key] = field_type

        # ``_optional_fields`` should be a list or tuple
        _optional_fields = attrs.get('_optional_fields', [])
        if _optional_fields is not None:
            if not isinstance(_optional_fields, (list, tuple)):
                raise ValueError('_optional_fields should be a list')

        if not _optional_fields:
            # try to use parent's _optional_fields
            for base in reversed(bases):
                if hasattr(base, '_optional_fields'):
                    _optional_fields.extend(base._optional_fields)

        klass = type.__new__(cls, name, bases, class_attrs)
        klass._fields = _fields
        klass._optional_fields = _optional_fields
        return klass


class Model(object, metaclass=ModelMeta):
    """base class for data models

    Usage::

        from april import Model

        class UserModel(Model):
            name = str
            title = str

            _optional_fields = ('title')

        user = UserModel(name='xxx')
        assert user.name == 'xxx'

        user2 = UserModel(user)
        assert user2.name = 'xxx'
    """
    def __init__(self, model=None, **kwargs):
        context = dict()
        fields_dict = self._fields

        if model is not None:
            for field_name, _ in self._fields.items():
                context[field_name] = getattr(model, field_name)

        context.update(kwargs)

        # check all requires fields
        for key, field_type in fields_dict.items():
            if key not in self._optional_fields and key not in context:
                raise ValueError("__init__ missing 1 required field: '{}'".format(key))

        for key, value in context.items():
            if key in fields_dict :
                field_type = fields_dict[key]
                # if value is not a field instance, try to deserialize
                if not isinstance(value, field_type):
                    new_value = self._deserialize_field(key, value)
                    self.__dict__[key] = new_value
                else:
                    self.__dict__[key] = value
            else:
                self.__dict__[key] = value

        # set all optional_fields value as None
        for field_name in self._optional_fields:
            if field_name not in self.__dict__:
                self.__dict__[field_name] = None

    @classmethod
    def is_field(cls, name):
        """check if a attribute belongs to model fields"""
        return name in dict(cls._fields)

    @classmethod
    def _deserialize_field(cls, name, value):
        field_type = dict(cls._fields)[name]
        if issubclass(field_type, Model):
            new_value = field_type(**value)
        elif is_nested_type(field_type):
            new_value = []
            for each in value:
                if not isinstance(each, field_type.nested_type):
                    new_value.append(field_type.nested_type(**each))
            if not new_value:
                new_value = value
        else :
            raise ValueError("field {} should be {}, got {}"
                             .format(name, field_type, type(value)))
        return new_value
