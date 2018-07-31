import datetime
import enum
import typing as t

import middle
import pytest
from middle.exceptions import InvalidType

from middle_schema.openapi import OpenAPI
from middle_schema.openapi import parse


def test_simple_model():
    class TestModel(middle.Model):
        name = middle.field(type=str, description="The name", min_length=5)

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name",
                    "minLength": 5,
                }
            },
            "type": "object",
            "required": ["name"],
        }
    }


def test_simple_model_with_typing():
    class TestModel(middle.Model):
        __description__ = "Test model for unit tests"
        name = middle.field(
            type=t.List[str], description="List of names", default=[]
        )

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {
                "name": {
                    "type": "array",
                    "description": "List of names",
                    "items": {"type": "string"},
                }
            },
            "description": "Test model for unit tests",
            "type": "object",
            "required": [],
        }
    }


def test_enum_choices():
    @enum.unique
    class TestIntEnum(enum.IntEnum):
        TEST_1 = 1
        TEST_2 = 2
        TEST_3 = 3

    class TestModel(middle.Model):
        some_enum = middle.field(
            type=TestIntEnum, description="Some test enumeration"
        )

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {
                "some_enum": {
                    "$ref": "#/components/schemas/TestIntEnum",
                    "description": "Some test enumeration",
                }
            },
            "type": "object",
            "required": ["some_enum"],
        },
        "TestIntEnum": {
            "type": "integer",
            "format": "int64",
            "choices": [1, 2, 3],
        },
    }


def test_enum_choices_no_component():
    @enum.unique
    class TestIntEnum(enum.IntEnum):
        TEST_1 = 1
        TEST_2 = 2
        TEST_3 = 3

    class TestModel(middle.Model):
        some_enum = middle.field(type=TestIntEnum)

    with middle.config.temp(openapi_enum_as_component=False):
        api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {
                "some_enum": {
                    "type": "integer",
                    "format": "int64",
                    "choices": [1, 2, 3],
                }
            },
            "type": "object",
            "required": ["some_enum"],
        }
    }


def test_dict_type():
    class TestModel(middle.Model):
        options = middle.field(
            type=t.Dict[str, str],
            description="Options for TestModel",
            min_properties=1,
        )

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {
                "options": {
                    "type": "object",
                    "description": "Options for TestModel",
                    "minProperties": 1,
                    "additionalProperties": {"type": "string"},
                }
            },
            "type": "object",
            "required": ["options"],
        }
    }


def test_invalid_dict_type():
    class TestModel(middle.Model):
        options = middle.field(type=t.Dict[float, str])

    with pytest.raises(TypeError):
        parse(TestModel)


def test_invalid_type_for_schema():
    class TestModel(middle.Model):
        name = middle.field(type=t.Tuple[str, int])

    with pytest.raises(InvalidType):
        parse(TestModel)


def test_optional_type():
    class TestModel(middle.Model):
        maybe_name = middle.field(type=t.Optional[str])

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {"maybe_name": {"type": "string", "nullable": True}},
            "type": "object",
            "required": [],
        }
    }


def test_union_type_nullable():
    class TestModel(middle.Model):
        lots_of_values = middle.field(type=t.Union[None, str, int])

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {
                "lots_of_values": {
                    "nullable": True,
                    "anyOf": [
                        {"type": "string"},
                        {"type": "integer", "format": "int64"},
                    ],
                }
            },
            "type": "object",
            "required": [],
        }
    }


def test_union_type_not_nullable():
    class TestModel(middle.Model):
        lots_of_values = middle.field(type=t.Union[str, int, float])

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {
                "lots_of_values": {
                    "anyOf": [
                        {"type": "string"},
                        {"type": "integer", "format": "int64"},
                        {"type": "number", "format": "double"},
                    ]
                }
            },
            "type": "object",
            "required": ["lots_of_values"],
        }
    }


def test_bool_type():
    class TestModel(middle.Model):
        switch = middle.field(type=bool)

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {"switch": {"type": "boolean"}},
            "type": "object",
            "required": ["switch"],
        }
    }


def test_byte_type():
    class TestModel(middle.Model):
        file_data = middle.field(
            type=bytes, description="The contents of the file"
        )

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {
                "file_data": {
                    "type": "string",
                    "format": "byte",
                    "description": "The contents of the file",
                }
            },
            "type": "object",
            "required": ["file_data"],
        }
    }


def test_date_type():
    class TestModel(middle.Model):
        when = middle.field(type=datetime.date)

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {"when": {"type": "string", "format": "date"}},
            "type": "object",
            "required": ["when"],
        }
    }


def test_datetime_type():
    class TestModel(middle.Model):
        when = middle.field(type=datetime.datetime)

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "TestModel": {
            "properties": {"when": {"type": "string", "format": "date-time"}},
            "type": "object",
            "required": ["when"],
        }
    }


def test_model_within_model():
    class InnerModel(middle.Model):
        name = middle.field(
            type=str, min_length=3, description="The person name"
        )
        age = middle.field(type=int, minimum=18, description="The person age")

    class TestModel(middle.Model):
        person = middle.field(
            type=InnerModel, description="The person to access this resource"
        )
        active = middle.field(
            type=bool, description="If the resource is active"
        )

    api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {"$ref": "#/components/schemas/TestModel"}
    assert api.components == {
        "InnerModel": {
            "properties": {
                "name": {
                    "type": "string",
                    "minLength": 3,
                    "description": "The person name",
                },
                "age": {
                    "type": "integer",
                    "format": "int64",
                    "minimum": 18,
                    "description": "The person age",
                },
            },
            "description": "The person to access this resource",
            "type": "object",
            "required": ["name", "age"],
        },
        "TestModel": {
            "properties": {
                "person": {"$ref": "#/components/schemas/InnerModel"},
                "active": {
                    "type": "boolean",
                    "description": "If the resource is active",
                },
            },
            "type": "object",
            "required": ["person", "active"],
        },
    }


def test_model_within_model_not_as_component():
    class InnerModel(middle.Model):
        name = middle.field(
            type=str, min_length=3, description="The person name"
        )
        age = middle.field(type=int, minimum=18, description="The person age")

    class TestModel(middle.Model):
        person = middle.field(
            type=InnerModel, description="The person to access this resource"
        )
        active = middle.field(
            type=bool, description="If the resource is active"
        )

    with middle.config.temp(openapi_model_as_component=False):
        api = parse(TestModel)

    assert isinstance(api, OpenAPI)
    assert api.specification == {
        "properties": {
            "person": {
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 3,
                        "description": "The person name",
                    },
                    "age": {
                        "type": "integer",
                        "format": "int64",
                        "minimum": 18,
                        "description": "The person age",
                    },
                },
                "description": "The person to access this resource",
                "type": "object",
                "required": ["name", "age"],
            },
            "active": {
                "type": "boolean",
                "description": "If the resource is active",
            },
        },
        "type": "object",
        "required": ["person", "active"],
    }
    assert api.components == {}
