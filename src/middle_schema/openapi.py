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
from .utils import is_model
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
    if skeleton.name is not None and not is_model(skeleton.type):
        if skeleton.validator_data.rules is not None:
            return {
                snake_to_camel_case(k): v
                for k, v in skeleton.validator_data.rules.items()
            }
    return {}


def _merge_keywords(skeleton):
    output = _get_validators(skeleton)
    if skeleton.description is not None:
        output["description"] = skeleton.description
    return output


def _parse_skeleton(skeleton, components):
    return _parse_type(skeleton.type, skeleton, components)


def _parse_model(type_, skeleton, components):
    children = {}
    for c in skeleton.children:
        o, components = _parse_skeleton(c, components)
        children.update({c.name: o})
    output = {
        "type": "object",
        "properties": children,
        "required": [
            c.name
            for c in filter(
                lambda s: not s.nullable and not s.has_default_value,
                skeleton.children,
            )
        ],
    }
    if skeleton.description is not None:
        output["description"] = skeleton.description
    if middle.config.openapi_model_as_component:
        components[type_.__name__] = output
        output = {"$ref": _component_name(type_.__name__)}
    return output, components


@type_dispatch()
def _parse_type(type_, skeleton, components):
    raise InvalidType()  # noqa will it get here after skel?


@_parse_type.register(middle.Model)  # for recursive types
@_parse_type.register(ModelMeta)  # for recursive types
def _parse_model_meta(type_, skeleton, components):
    return _parse_model(type_, skeleton, components)


@_parse_type.register(str)
def _parse_type_str(type_, skeleton, components):
    return {"type": "string", **_merge_keywords(skeleton)}, components


@_parse_type.register(bytes)
def _parse_type_bytes(type_, skeleton, components):
    return (
        {"type": "string", "format": "byte", **_merge_keywords(skeleton)},
        components,
    )


@_parse_type.register(int)
def _parse_type_int(type_, skeleton, components):
    return (
        {"type": "integer", "format": "int64", **_merge_keywords(skeleton)},
        components,
    )


@_parse_type.register(float)
@_parse_type.register(Decimal)
def _parse_type_number(type_, skeleton, components):
    return (
        {"type": "number", "format": "double", **_merge_keywords(skeleton)},
        components,
    )


@_parse_type.register(bool)
def _parse_type_bool(type_, skeleton, components):
    return {"type": "boolean", **_merge_keywords(skeleton)}, components


@_parse_type.register(datetime.date)
def _parse_type_date(type_, skeleton, components):
    return (
        {"type": "string", "format": "date", **_merge_keywords(skeleton)},
        components,
    )


@_parse_type.register(datetime.datetime)
def _parse_type_datetime(type_, skeleton, components):
    return (
        {"type": "string", "format": "date-time", **_merge_keywords(skeleton)},
        components,
    )


@_parse_type.register(EnumMeta)
def _parse_type_enum(type_, skeleton, components):
    choices = skeleton.type_specific.get("choices")
    output, components = _parse_type(type(choices[0]), skeleton, components)
    output["choices"] = choices
    if middle.config.openapi_enum_as_component:
        description = output.pop("description")
        components[type_.__name__] = output
        output = {"$ref": _component_name(type_.__name__)}
        if description is not None:
            output["description"] = description
    return output, components


@_parse_type.register(typing.List)
@_parse_type.register(typing.Set)
def _parse_type_iterable_set(type_, skeleton, components):
    output, components = _parse_skeleton(skeleton.children[0], components)
    return (
        {"type": "array", "items": {**output}, **_merge_keywords(skeleton)},
        components,
    )


@_parse_type.register(typing.Dict)
def _parse_type_dict(type_, skeleton, components):
    output, components = _parse_skeleton(skeleton.children[0], components)
    return (
        {
            "type": "object",
            "additionalProperties": output,
            **_merge_keywords(skeleton),
        },
        components,
    )


@_parse_type.register(typing.Union)
def _parse_type_union(type_, skeleton, components):
    output = {}
    if skeleton.type_specific is not None and skeleton.type_specific.get(
        "any_of", False
    ):
        any_of = []
        for s in skeleton.children:
            o, components = _parse_skeleton(s, components)
            any_of.append(o)
        output["anyOf"] = any_of
    else:
        output, components = _parse_skeleton(skeleton.children[0], components)
    if skeleton.nullable:
        output["nullable"] = True
    output.update(**_merge_keywords(skeleton))
    return output, components
