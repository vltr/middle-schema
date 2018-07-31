import datetime
import inspect
import typing
from decimal import Decimal
from enum import EnumMeta

import attr
import middle
from attr._make import NOTHING  # NOTE: this is internal to attrs
from attr._make import Attribute  # NOTE: this is internal to attrs
from attr._make import _AndValidator
from attr.validators import _InstanceOfValidator
from middle.compat import NoneType
from middle.dispatch import type_dispatch
from middle.exceptions import InvalidType
from middle.model import ModelMeta
from middle.validators import BaseValidator

from .utils import is_model

_sentinel = object()


# --------------------------------------------------------------------------- #
# Validator related data
# --------------------------------------------------------------------------- #


@attr.s
class ValidatorData:
    rules = attr.ib(type=dict, default=None)
    type_check = attr.ib(default=None)


# --------------------------------------------------------------------------- #
# Skeleton class for very basic types (usually List, Dict, Union args)
# --------------------------------------------------------------------------- #


@attr.s
class Skeleton:
    type = attr.ib()
    default_value = attr.ib(default=_sentinel)
    validator_data = attr.ib(type=ValidatorData, default=None)
    name = attr.ib(type=str, default=None)
    type_specific = attr.ib(type=dict, default=None)
    description = attr.ib(type=str, default=None)
    children = attr.ib(type=list, default=None)
    nullable = attr.ib(type=bool, default=False)

    @property
    def has_default_value(self):
        return (
            self.default_value != NOTHING and self.default_value != _sentinel
        )


# --------------------------------------------------------------------------- #
# Translate models to skeletons
# --------------------------------------------------------------------------- #


def translate(field, model_or_field=None):
    if isinstance(field, Attribute):
        return _translate_type(field.type, field)
    else:
        return _translate_type(field, model_or_field)


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #


def _is_field(model_or_field):
    return isinstance(model_or_field, Attribute)


def _get_default_value(model_or_field):
    if _is_field(model_or_field):
        return model_or_field.default
    return NOTHING


def _get_skel_name(model_or_field, extra_field=None):
    if extra_field is not None:
        return _get_skel_name(extra_field, None)
    if _is_field(model_or_field):
        return model_or_field.name
    elif is_model(model_or_field):
        return model_or_field.__name__
    else:  # noqa if it get's here (not if based on middle)
        return str(model_or_field)


def _get_validator_data(field):
    data = {}
    if isinstance(field, Attribute):
        if isinstance(field.validator, _AndValidator):
            for validator in field.validator._validators:
                if isinstance(validator, BaseValidator):
                    data["rules"] = validator.descriptor
                elif isinstance(validator, _InstanceOfValidator):
                    data["type_check"] = validator.type
        else:
            if isinstance(field.validator, BaseValidator):
                data["rules"] = field.validator.descriptor
            elif isinstance(field.validator, _InstanceOfValidator):
                data["type_check"] = field.validator.type
    return ValidatorData(
        rules=data.get("rules"), type_check=data.get("type_check")
    )


def _get_model_description(model):
    if hasattr(model, "__description__") and isinstance(
        model.__description__, str
    ):
        return model.__description__
    return inspect.getdoc(model)


def _get_attr_description(field):
    if field is None:
        return None
    return field.metadata.get("description", None)


# --------------------------------------------------------------------------- #
# Creating component parsers
# --------------------------------------------------------------------------- #


@type_dispatch()
def _translate_type(type_, model_or_field):
    raise InvalidType()


# --------------------------------------------------------------------------- #
# Recursive (Model) types
# --------------------------------------------------------------------------- #


@_translate_type.register(middle.Model)
@_translate_type.register(ModelMeta)
def _translate_model_meta(type_, model_or_field):
    return Skeleton(
        name=_get_skel_name(type_, model_or_field),
        description=_get_model_description(type_)
        or _get_attr_description(model_or_field),
        type=type_,
        default_value=_get_default_value(model_or_field),
        children=[translate(field, type_) for field in attr.fields(type_)],
    )


# --------------------------------------------------------------------------- #
# All (simple) types available
# --------------------------------------------------------------------------- #


@_translate_type.register(str)
@_translate_type.register(bytes)
@_translate_type.register(int)
@_translate_type.register(float)
@_translate_type.register(Decimal)
@_translate_type.register(bool)
@_translate_type.register(datetime.date)
@_translate_type.register(datetime.datetime)
def _translate_type_generic(type_, model_or_field):
    if model_or_field is None:
        return Skeleton(type=type_)
    return Skeleton(
        name=_get_skel_name(model_or_field),
        description=_get_attr_description(model_or_field),
        type=type_,
        default_value=_get_default_value(model_or_field),
        validator_data=_get_validator_data(model_or_field),
    )


# --------------------------------------------------------------------------- #
# Most complex types
# --------------------------------------------------------------------------- #


@_translate_type.register(EnumMeta)
def _translate_type_enum(type_, model_or_field):
    choices = [e.value for e in type_]
    return Skeleton(
        name=_get_skel_name(model_or_field),
        description=_get_attr_description(model_or_field),
        default_value=_get_default_value(model_or_field),
        validator_data=_get_validator_data(model_or_field),
        children=[translate(type(choices[0]), None)],
        type=type_,
        type_specific={"choices": choices},
    )


@_translate_type.register(typing.List)
@_translate_type.register(typing.Set)
def _translate_type_iterable_set(type_, model_or_field):
    return Skeleton(
        name=_get_skel_name(model_or_field),
        description=_get_attr_description(model_or_field),
        default_value=_get_default_value(model_or_field),
        type=type_,
        validator_data=_get_validator_data(model_or_field),
        children=[translate(type_.__args__[0], None)],
    )


@_translate_type.register(typing.Dict)
def _translate_type_dict(type_, model_or_field):
    if type_.__args__[0] == str:
        return Skeleton(
            name=_get_skel_name(model_or_field),
            description=_get_attr_description(model_or_field),
            default_value=_get_default_value(model_or_field),
            type=type_,
            validator_data=_get_validator_data(model_or_field),
            children=[translate(type_.__args__[1], None)],
        )

    else:
        raise TypeError(
            "For better API integration, it is better to always have `str` as "
            "the first argument on Dict, eg: Dict[str, other_type]"
        )


@_translate_type.register(typing.Union)
def _translate_type_union(type_, model_or_field):
    if NoneType in type_.__args__:
        if len(type_.__args__) == 2:  # Optional
            arg = list(filter(lambda a: a is not NoneType, type_.__args__))[0]
            return Skeleton(
                name=_get_skel_name(model_or_field),
                description=_get_attr_description(model_or_field),
                default_value=_get_default_value(model_or_field),
                type=type_,
                validator_data=_get_validator_data(model_or_field),
                children=[translate(arg, None)],
                nullable=True,
            )
        else:
            return Skeleton(
                name=_get_skel_name(model_or_field),
                description=_get_attr_description(model_or_field),
                default_value=_get_default_value(model_or_field),
                type=type_,
                validator_data=_get_validator_data(model_or_field),
                children=[
                    translate(arg, None)
                    for arg in type_.__args__
                    if arg is not NoneType
                ],
                nullable=True,
                type_specific={"any_of": True},
            )

    return Skeleton(
        name=_get_skel_name(model_or_field),
        description=_get_attr_description(model_or_field),
        # field=model_or_field,
        default_value=_get_default_value(model_or_field),
        type=type_,
        validator_data=_get_validator_data(model_or_field),
        children=[translate(arg, None) for arg in type_.__args__],
        type_specific={"any_of": True},
    )
