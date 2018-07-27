import datetime
import typing
from decimal import Decimal
from enum import EnumMeta

import attr
import middle
from middle.dispatch import type_dispatch
from middle.exceptions import InvalidType
from middle.model import ModelMeta

from .skel import translate
from .utils import raise_simple_type
from .utils import snake_to_camel_case


@attr.s
class OpenAPI:
    components = attr.ib(default=dict)
    specification = attr.ib(default=dict)


def parse(model_or_field):
    specs, components = _parse_skeleton(translate(model_or_field), {})
    return OpenAPI(components=components, specification=specs)


def _component_name(name):
    return "#/components/schemas/{}".format(name)


def _get_validators(skeleton):
    if skeleton.is_field:
        if skeleton.validator_data.rules is not None:
            return {
                snake_to_camel_case(k): v
                for k, v in skeleton.validator_data.rules.items()
            }
    return {}


def _parse_skeleton(skeleton, components):
    return _parse_type(skeleton.of_type, skeleton, components)


def _parse_model(type_, skeleton, components):
    children = {}
    for c in skeleton.children:
        o, components = _parse_skeleton(c, components)
        children.update({c.name: o})
    output = {
        "type": "object",
        "description": skeleton.description,
        "properties": children,
        "required": [
            c.name for c in filter(lambda s: not s.nullable, skeleton.children)
        ],
    }
    if middle.config.openapi_model_as_component:
        components[skeleton.name] = output
        output = {"$ref": _component_name(skeleton.name)}
    return output, components


@type_dispatch()
def _parse_type(type_, skeleton, components):
    raise InvalidType()


@_parse_type.register(middle.Model)  # for recursive types
@_parse_type.register(ModelMeta)  # for recursive types
def _parse_model_meta(type_, skeleton, components):
    return _parse_model(type_, skeleton, components)


@_parse_type.register(list)
@_parse_type.register(set)
def _parse_type_simple_iterables(type_, skeleton, components):
    raise_simple_type(type_, typing.List, typing.Set)


@_parse_type.register(dict)
def _parse_type_simple_dict(type_, skeleton, components):
    raise_simple_type(type_, typing.Dict)


@_parse_type.register(str)
def _parse_type_str(type_, skeleton, components):
    return {"type": "string", **_get_validators(skeleton)}, components


@_parse_type.register(bytes)
def _parse_type_bytes(type_, skeleton, components):
    return (
        {"type": "string", "format": "byte", **_get_validators(skeleton)},
        components,
    )


@_parse_type.register(int)
def _parse_type_int(type_, skeleton, components):
    return (
        {"type": "integer", "format": "int64", **_get_validators(skeleton)},
        components,
    )


@_parse_type.register(float)
@_parse_type.register(Decimal)
def _parse_type_number(type_, skeleton, components):
    return (
        {"type": "number", "format": "double", **_get_validators(skeleton)},
        components,
    )


@_parse_type.register(bool)
def _parse_type_bool(type_, skeleton, components):
    return {"type": "boolean"}, components


@_parse_type.register(datetime.date)
def _parse_type_date(type_, skeleton, components):
    return {"type": "string", "format": "date"}, components


@_parse_type.register(datetime.datetime)
def _parse_type_datetime(type_, skeleton, components):
    return {"type": "string", "format": "date-time"}, components


@_parse_type.register(EnumMeta)
def _parse_type_enum(type_, skeleton, components):
    choices = skeleton.type_specific.get("choices")
    output, components = _parse_type(type(choices[0]), skeleton, components)
    output["choices"] = choices
    if middle.config.openapi_enum_as_component:
        components[type_.__name__] = output
        output = {"$ref": _component_name(type_.__name__)}
    return output, components


@_parse_type.register(typing.List)
@_parse_type.register(typing.Set)
def _parse_type_iterable_set(type_, skeleton, components):
    output, components = _parse_skeleton(skeleton.children[0], components)
    return (
        {"type": "array", "items": {**output}, **_get_validators(skeleton)},
        components,
    )


@_parse_type.register(typing.Dict)
def _parse_type_dict(type_, skeleton, components):
    output, components = _parse_skeleton(skeleton.children[0], components)
    return ({"type": "object", "additionalProperties": output}, components)


@_parse_type.register(typing.Union)
def _parse_type_union(type_, skeleton, components):
    output = {}
    if skeleton.type_specific.get("any_of", False):
        any_of = []
        for s in skeleton.children:
            o, components = _parse_skeleton(s, components)
            any_of.append(o)
        output["anyOf"] = any_of
    else:
        output, components = _parse_skeleton(skeleton.children[0], components)
    if skeleton.nullable:
        output["nullable"] = True
    return output, components


# TODO: I don't think I can order the types in the OpenAPI spec, can I ?
# @_serialize_type.register(typing.Tuple)
# def _serialize_type_tuple(type_):
#     return partial(
#         _multiple_types_serialize_type_ordered,
#         [_serialize_type(arg) for arg in type_.__args__],
#     )
