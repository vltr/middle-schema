import enum
import typing as t

import middle
import pytest
from middle.exceptions import InvalidType

from middle_schema.skel import ComplexSkeleton
from middle_schema.skel import Skeleton
from middle_schema.skel import translate


def test_simple_model():
    class TestModel(middle.Model):
        name = middle.field(type=str, description="The name", min_length=5)

    skel = translate(TestModel)

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == TestModel
    assert skel.is_model
    assert not skel.is_field
    assert not skel.has_default_value
    assert skel.name == "TestModel"
    assert skel.description is None
    assert not skel.nullable
    assert skel.validator_data is None

    skel = skel.children[0]

    assert isinstance(skel, ComplexSkeleton)
    assert skel.children is None
    assert skel.of_type == str
    assert not skel.is_model
    assert skel.is_field
    assert not skel.has_default_value
    assert skel.name == "name"
    assert skel.description == "The name"
    assert not skel.nullable
    assert skel.validator_data is not None
    assert skel.validator_data.has_rules
    assert skel.validator_data.has_type_check
    assert skel.validator_data.rules == {"min_length": 5}


def test_simple_model_with_typing():
    class TestModel(middle.Model):
        __description__ = "Test model for unit tests"
        name = middle.field(
            type=t.List[str], description="List of names", default=[]
        )

    skel = translate(TestModel)

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == TestModel
    assert skel.is_model
    assert not skel.is_field
    assert not skel.has_default_value
    assert skel.name == "TestModel"
    assert skel.description == "Test model for unit tests"
    assert not skel.nullable
    assert skel.validator_data is None

    skel = skel.children[0]

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == t.List[str]
    assert not skel.is_model
    assert skel.is_field
    assert skel.has_default_value
    assert skel.name == "name"
    assert skel.description == "List of names"
    assert skel.nullable
    assert skel.validator_data is not None
    assert not skel.validator_data.has_rules
    assert skel.validator_data.has_type_check
    assert skel.validator_data.of_type == list

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert skel.children is None
    assert skel.of_type == str
    assert not skel.is_model
    assert not skel.is_field
    assert not skel.has_default_value


def test_enum_choices():
    @enum.unique
    class TestIntEnum(enum.IntEnum):
        TEST_1 = 1
        TEST_2 = 2
        TEST_3 = 3

    class TestModel(middle.Model):
        some_enum = middle.field(type=TestIntEnum)

    skel = translate(TestModel)

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == TestModel
    assert skel.is_model
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == TestIntEnum
    assert not skel.is_model
    assert skel.is_field
    assert not skel.has_default_value
    assert skel.name == "some_enum"
    assert skel.description is None
    assert not skel.nullable
    assert skel.validator_data is not None
    assert not skel.validator_data.has_rules
    assert skel.validator_data.has_type_check
    assert skel.validator_data.of_type == TestIntEnum
    assert skel.type_specific is not None
    assert skel.type_specific == {"choices": [1, 2, 3]}

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert skel.children is None
    assert skel.of_type == int
    assert not skel.is_model
    assert not skel.is_field
    assert not skel.has_default_value


def test_dict_type():
    class TestModel(middle.Model):
        options = middle.field(
            type=t.Dict[str, str],
            description="Options for TestModel",
            min_properties=1,
        )

    skel = translate(TestModel)

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == TestModel
    assert skel.is_model
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == t.Dict[str, str]
    assert not skel.is_model
    assert skel.is_field
    assert not skel.has_default_value
    assert skel.name == "options"
    assert skel.description == "Options for TestModel"
    assert not skel.nullable
    assert skel.validator_data is not None
    assert skel.validator_data.has_rules
    assert skel.validator_data.has_type_check
    assert skel.validator_data.of_type == dict
    assert skel.validator_data.rules == {"min_properties": 1}
    assert skel.type_specific is None

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert skel.children is None
    assert skel.of_type == str
    assert not skel.is_model
    assert not skel.is_field
    assert not skel.has_default_value


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

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == TestModel
    assert skel.is_model
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == t.Union[str, middle.compat.NoneType]
    assert not skel.is_model
    assert skel.is_field
    assert not skel.has_default_value
    assert skel.name == "maybe_name"
    assert skel.description is None
    assert skel.nullable
    assert skel.validator_data is not None
    assert not skel.validator_data.has_rules
    assert skel.validator_data.has_type_check
    assert skel.validator_data.of_type == (str, middle.compat.NoneType)
    assert skel.validator_data.rules is None
    assert skel.type_specific is None

    skel = skel.children[0]

    assert isinstance(skel, Skeleton)
    assert skel.children is None
    assert skel.of_type == str
    assert not skel.is_model
    assert skel.is_field
    assert not skel.has_default_value


def test_union_type_nullable():
    class TestModel(middle.Model):
        lots_of_values = middle.field(type=t.Union[None, str, int])

    skel = translate(TestModel)

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == TestModel
    assert skel.is_model
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 2
    assert skel.of_type == t.Union[middle.compat.NoneType, str, int]
    assert not skel.is_model
    assert skel.is_field
    assert not skel.has_default_value
    assert skel.name == "lots_of_values"
    assert skel.description is None
    assert skel.nullable
    assert skel.validator_data is not None
    assert not skel.validator_data.has_rules
    assert skel.validator_data.has_type_check
    assert skel.validator_data.of_type == (middle.compat.NoneType, str, int)
    assert skel.validator_data.rules is None
    assert skel.type_specific == {"any_of": True}

    skel_str = skel.children[0]

    assert isinstance(skel_str, Skeleton)
    assert skel_str.children is None
    assert skel_str.of_type == str
    assert not skel_str.is_model
    assert skel_str.is_field
    assert not skel_str.has_default_value

    skel_int = skel.children[1]

    assert isinstance(skel_int, Skeleton)
    assert skel_int.children is None
    assert skel_int.of_type == int
    assert not skel_int.is_model
    assert skel_int.is_field
    assert not skel_int.has_default_value


def test_union_type_not_nullable():
    class TestModel(middle.Model):
        lots_of_values = middle.field(type=t.Union[str, int, float])

    skel = translate(TestModel)

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 1
    assert skel.of_type == TestModel
    assert skel.is_model
    assert skel.name == "TestModel"

    skel = skel.children[0]

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 3
    assert skel.of_type == t.Union[str, int, float]
    assert not skel.is_model
    assert skel.is_field
    assert not skel.has_default_value
    assert skel.name == "lots_of_values"
    assert skel.description is None
    assert not skel.nullable
    assert skel.validator_data is not None
    assert not skel.validator_data.has_rules
    assert skel.validator_data.has_type_check
    assert skel.validator_data.of_type == (str, int, float)
    assert skel.validator_data.rules is None
    assert skel.type_specific == {"any_of": True}

    skel_str = skel.children[0]

    assert isinstance(skel_str, Skeleton)
    assert skel_str.children is None
    assert skel_str.of_type == str
    assert not skel_str.is_model
    assert skel_str.is_field
    assert not skel_str.has_default_value

    skel_int = skel.children[1]

    assert isinstance(skel_int, Skeleton)
    assert skel_int.children is None
    assert skel_int.of_type == int
    assert not skel_int.is_model
    assert skel_int.is_field
    assert not skel_int.has_default_value

    skel_float = skel.children[2]

    assert isinstance(skel_float, Skeleton)
    assert skel_float.children is None
    assert skel_float.of_type == float
    assert not skel_float.is_model
    assert skel_float.is_field
    assert not skel_float.has_default_value
