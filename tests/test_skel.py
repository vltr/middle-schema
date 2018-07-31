import enum
import typing as t

import middle
import pytest
from middle.exceptions import InvalidType

from middle_schema.skel import Skeleton
from middle_schema.skel import translate


def test_simple_model():
    class TestModel(middle.Model):
        name = middle.field(type=str, description="The name", min_length=5)

    skel = translate(TestModel)

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == TestModel
    assert not skel.has_default_value
    assert skel.name == "TestModel"
    assert skel.description is None
    assert not skel.nullable
    assert skel.validator_data is None

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert skel.children is None
    assert skel.type == str
    assert not skel.has_default_value
    assert skel.name == "name"
    assert skel.description == "The name"
    assert not skel.nullable
    assert skel.validator_data.rules == {"min_length": 5}
    assert skel.validator_data.type_check == str


def test_simple_model_with_typing():
    class TestModel(middle.Model):
        __description__ = "Test model for unit tests"
        name = middle.field(
            type=t.List[str], description="List of names", default=[]
        )

    skel = translate(TestModel)

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == TestModel
    assert not skel.has_default_value
    assert skel.name == "TestModel"
    assert skel.description == "Test model for unit tests"
    assert not skel.nullable
    assert skel.validator_data is None

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == t.List[str]
    assert skel.has_default_value
    assert skel.default_value == []
    assert skel.name == "name"
    assert skel.description == "List of names"
    assert not skel.nullable
    assert skel.validator_data.rules is None
    assert skel.validator_data.type_check == list

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert skel.children is None
    assert skel.type == str
    assert not skel.has_default_value
    assert skel.validator_data is None
    assert skel.name is None
    assert skel.type_specific is None
    assert skel.description is None
    assert skel.nullable is False


def test_enum_choices():
    @enum.unique
    class TestIntEnum(enum.IntEnum):
        TEST_1 = 1
        TEST_2 = 2
        TEST_3 = 3

    class TestModel(middle.Model):
        some_enum = middle.field(type=TestIntEnum)

    skel = translate(TestModel)

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == TestModel
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == TestIntEnum
    assert skel.name == "some_enum"
    assert skel.description is None
    assert not skel.nullable
    assert skel.validator_data.rules is None
    assert skel.validator_data.type_check == TestIntEnum
    assert skel.type_specific is not None
    assert skel.type_specific == {"choices": [1, 2, 3]}

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert skel.children is None
    assert skel.type == int
    assert not skel.has_default_value
    assert skel.validator_data is None
    assert skel.name is None
    assert skel.type_specific is None
    assert skel.description is None
    assert skel.nullable is False


def test_dict_type():
    class TestModel(middle.Model):
        options = middle.field(
            type=t.Dict[str, str],
            description="Options for TestModel",
            min_properties=1,
        )

    skel = translate(TestModel)

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == TestModel
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == t.Dict[str, str]
    assert not skel.has_default_value
    assert skel.name == "options"
    assert skel.description == "Options for TestModel"
    assert not skel.nullable
    assert skel.validator_data.type_check == dict
    assert skel.validator_data.rules == {"min_properties": 1}
    assert skel.type_specific is None

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert skel.children is None
    assert skel.type == str
    assert not skel.has_default_value
    assert skel.validator_data is None
    assert skel.name is None
    assert skel.type_specific is None
    assert skel.description is None
    assert skel.nullable is False


def test_invalid_dict_type():
    class TestModel(middle.Model):
        options = middle.field(type=t.Dict[float, str])

    with pytest.raises(TypeError):
        translate(TestModel)


def test_invalid_type_for_schema():
    class TestModel(middle.Model):
        name = middle.field(type=t.Tuple[str, int])

    with pytest.raises(InvalidType):
        translate(TestModel)


def test_optional_type():
    class TestModel(middle.Model):
        maybe_name = middle.field(type=t.Optional[str])

    skel = translate(TestModel)

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == TestModel
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == t.Union[str, middle.compat.NoneType]
    assert not skel.has_default_value
    assert skel.name == "maybe_name"
    assert skel.description is None
    assert skel.nullable
    assert skel.validator_data.type_check == (str, middle.compat.NoneType)
    assert skel.validator_data.rules is None
    assert skel.type_specific is None

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert skel.children is None
    assert skel.type == str
    assert not skel.has_default_value
    assert skel.validator_data is None
    assert skel.name is None
    assert skel.type_specific is None
    assert skel.description is None
    assert skel.nullable is False


def test_union_type_nullable():
    class TestModel(middle.Model):
        lots_of_values = middle.field(type=t.Union[None, str, int])

    skel = translate(TestModel)

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == TestModel
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 2
    assert skel.type == t.Union[middle.compat.NoneType, str, int]
    assert not skel.has_default_value
    assert skel.name == "lots_of_values"
    assert skel.description is None
    assert skel.nullable
    assert skel.validator_data.type_check == (middle.compat.NoneType, str, int)
    assert skel.validator_data.rules is None
    assert skel.type_specific == {"any_of": True}

    skel_str = skel.children[0]

    assert isinstance(skel_str, Skeleton)
    assert skel_str.children is None
    assert skel_str.type == str
    assert not skel_str.has_default_value
    assert skel_str.validator_data is None
    assert skel_str.name is None
    assert skel_str.type_specific is None
    assert skel_str.description is None
    assert skel_str.nullable is False

    skel_int = skel.children[1]

    assert isinstance(skel_int, Skeleton)
    assert skel_int.children is None
    assert skel_int.type == int
    assert not skel_int.has_default_value
    assert skel_int.validator_data is None
    assert skel_int.name is None
    assert skel_int.type_specific is None
    assert skel_int.description is None
    assert skel_int.nullable is False


def test_union_type_not_nullable():
    class TestModel(middle.Model):
        lots_of_values = middle.field(type=t.Union[str, int, float])

    skel = translate(TestModel)

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 1
    assert skel.type == TestModel
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 3
    assert skel.type == t.Union[str, int, float]
    assert not skel.has_default_value
    assert skel.name == "lots_of_values"
    assert skel.description is None
    assert not skel.nullable
    assert skel.validator_data.type_check == (str, int, float)
    assert skel.validator_data.rules is None
    assert skel.type_specific == {"any_of": True}

    skel_str = skel.children[0]

    assert isinstance(skel_str, Skeleton)
    assert skel_str.children is None
    assert skel_str.type == str
    assert not skel_str.has_default_value
    assert skel_str.validator_data is None
    assert skel_str.name is None
    assert skel_str.type_specific is None
    assert skel_str.description is None
    assert skel_str.nullable is False

    skel_int = skel.children[1]

    assert isinstance(skel_int, Skeleton)
    assert skel_int.children is None
    assert skel_int.type == int
    assert not skel_int.has_default_value
    assert skel_int.validator_data is None
    assert skel_int.name is None
    assert skel_int.type_specific is None
    assert skel_int.description is None
    assert skel_int.nullable is False

    skel_float = skel.children[2]

    assert isinstance(skel_float, Skeleton)
    assert skel_float.children is None
    assert skel_float.type == float
    assert not skel_float.has_default_value
    assert skel_float.validator_data is None
    assert skel_float.name is None
    assert skel_float.type_specific is None
    assert skel_float.description is None
    assert skel_float.nullable is False
