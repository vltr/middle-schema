import enum
import typing as t

import middle

from middle_schema.skel import ComplexSkeleton
from middle_schema.skel import Skeleton
from middle_schema.skel import translate


@enum.unique
class PlatformEnum(str, enum.Enum):
    XBOX1 = "XBOX1"
    PLAYSTATION4 = "PLAYSTATION4"
    PC = "PC"


@enum.unique
class LanguageEnum(enum.IntEnum):
    ENGLISH = 1
    JAPANESE = 2
    SPANISH = 3
    GERMAN = 4
    PORTUGUESE = 5


@enum.unique
class CityRegionEnum(str, enum.Enum):
    TROPICAL = "TROPICAL"
    TEMPERATE = "TEMPERATE"
    BOREAL = "BOREAL"


class City(middle.Model):
    __description__ = "One awesome city built"
    name = middle.field(type=str, description="The city name")
    region = middle.field(
        default=CityRegionEnum.TEMPERATE,
        type=CityRegionEnum,
        description="The region this city is located",
    )


class Player(middle.Model):
    nickname = middle.field(
        type=str, description="The nickname of the player over the internet"
    )
    youtube_channel = middle.field(
        type=str, description="The YouTube channel of the player", default=None
    )


class Game(middle.Model):
    __description__ = "An electronic game model"

    name = middle.field(type=str, description="The name of the game")
    platform = middle.field(
        type=PlatformEnum, description="Which platform it runs on"
    )
    score = middle.field(
        type=float,
        description="The average score of the game",
        minimum=0,
        maximum=10,
        multiple_of=0.1,
    )
    resolution_tested = middle.field(
        type=str,
        description="The resolution which the game was tested",
        pattern="^\d+x\d+$",
    )
    genre = middle.field(
        type=t.List[str],
        description="One or more genres this game is part of",
        min_items=1,
        unique_items=True,
    )
    rating = middle.field(
        type=t.Dict[str, float],
        description="Ratings given on specialized websites",
        min_properties=3,
    )
    players = middle.field(
        type=t.Set[Player],
        description="Some of the notorious players of this game",
    )
    language = middle.field(
        type=LanguageEnum, description="The main language of the game"
    )
    awesome_city = middle.field(type=City)
    remarkable_resources = middle.field(
        type=t.Union[Player, City],
        description="Some remarkable resources of this game over the internet",
    )


def test_simple_model():

    skel = translate(Game)

    assert isinstance(skel, ComplexSkeleton)
    assert len(skel.children) == 10
    assert skel.of_type == Game
    assert skel.is_model
    assert not skel.is_field
    assert not skel.has_default_value
    assert skel.name == "Game"
    assert skel.description == "An electronic game model"
    assert not skel.nullable
    assert skel.validator_data is None

    for c in skel.children:
        if c.name == "name":
            assert isinstance(c, ComplexSkeleton)
            assert c.children is None
            assert c.of_type == str
            assert not c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert c.description == "The name of the game"
            assert not c.nullable
            assert c.validator_data is not None
            assert not c.validator_data.has_rules
            assert c.validator_data.has_type_check
            assert c.validator_data.rules is None
        if c.name == "platform":
            assert isinstance(c, ComplexSkeleton)
            assert len(c.children) == 1
            assert c.of_type == PlatformEnum
            assert not c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert c.description == "Which platform it runs on"
            assert not c.nullable
            assert c.validator_data is not None
            assert not c.validator_data.has_rules
            assert c.validator_data.has_type_check
            assert c.validator_data.rules is None
            assert c.type_specific is not None
            assert c.type_specific == {
                "choices": ["XBOX1", "PLAYSTATION4", "PC"]
            }
            # choices type
            assert isinstance(c.children[0], Skeleton)
            assert c.children[0].children is None
            assert c.children[0].of_type == str
            assert not c.children[0].is_model
            assert not c.children[0].is_field
            assert not c.children[0].has_default_value
        if c.name == "score":
            assert isinstance(c, ComplexSkeleton)
            assert c.children is None
            assert c.of_type == float
            assert not c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert c.description == "The average score of the game"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.has_rules
            assert c.validator_data.has_type_check
            assert c.validator_data.rules == {
                "minimum": 0,
                "maximum": 10,
                "multiple_of": 0.1,
            }
        if c.name == "resolution_tested":
            assert isinstance(c, ComplexSkeleton)
            assert c.children is None
            assert c.of_type == str
            assert not c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert c.description == "The resolution which the game was tested"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.has_rules
            assert c.validator_data.has_type_check
            assert c.validator_data.rules == {"pattern": "^\d+x\d+$"}
        if c.name == "genre":
            assert isinstance(c, ComplexSkeleton)
            assert len(c.children) == 1
            assert c.of_type == t.List[str]
            assert not c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert c.description == "One or more genres this game is part of"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.has_rules
            assert c.validator_data.has_type_check
            assert c.validator_data.of_type == list
            assert c.validator_data.rules == {
                "min_items": 1,
                "unique_items": True,
            }
            # inner list type
            assert isinstance(c.children[0], Skeleton)
            assert c.children[0].children is None
            assert c.children[0].of_type == str
            assert not c.children[0].is_model
            assert not c.children[0].is_field
            assert not c.children[0].has_default_value
        if c.name == "rating":
            assert isinstance(c, ComplexSkeleton)
            assert len(c.children) == 1
            assert c.of_type == t.Dict[str, float]
            assert not c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert c.description == "Ratings given on specialized websites"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.has_rules
            assert c.validator_data.has_type_check
            assert c.validator_data.of_type == dict
            assert c.validator_data.rules == {"min_properties": 3}
            # inner dict type
            assert isinstance(c.children[0], Skeleton)
            assert c.children[0].children is None
            assert c.children[0].of_type == float
            assert not c.children[0].is_model
            assert not c.children[0].is_field
            assert not c.children[0].has_default_value
        if c.name == "players":
            assert isinstance(c, ComplexSkeleton)
            assert len(c.children) == 1
            assert c.of_type == t.Set[Player]
            assert not c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert (
                c.description == "Some of the notorious players of this game"
            )
            assert not c.nullable
            assert c.validator_data is not None
            assert not c.validator_data.has_rules
            assert c.validator_data.has_type_check
            assert c.validator_data.of_type == set
            # inner set type
            ci = c.children[0]
            assert isinstance(ci, Skeleton)
            assert len(ci.children) == 2
            assert ci.of_type == Player
            assert ci.is_model
            assert not ci.is_field
            # inner model (complex type)
            for cj in ci.children:
                if cj.name == "nickname":
                    assert isinstance(c, ComplexSkeleton)
                    assert cj.children is None
                    assert cj.of_type == str
                    assert not cj.is_model
                    assert cj.is_field
                    assert not cj.has_default_value
                    assert (
                        cj.description
                        == "The nickname of the player over the internet"
                    )
                    assert not cj.nullable
                    assert cj.validator_data is not None
                    assert not cj.validator_data.has_rules
                    assert cj.validator_data.has_type_check
                    assert cj.validator_data.of_type == str
                    assert cj.validator_data.rules is None
                if cj.name == "youtube_channel":
                    assert isinstance(c, ComplexSkeleton)
                    assert cj.children is None
                    assert cj.of_type == str
                    assert not cj.is_model
                    assert cj.is_field
                    assert cj.has_default_value
                    assert cj.default is None
                    assert (
                        cj.description == "The YouTube channel of the player"
                    )
                    assert cj.nullable
                    assert cj.validator_data is not None
                    assert not cj.validator_data.has_rules
                    assert cj.validator_data.has_type_check
                    assert cj.validator_data.of_type == (
                        str,
                        middle.compat.NoneType,
                    )
                    assert cj.validator_data.rules is None
        if c.name == "language":
            assert isinstance(c, ComplexSkeleton)
            assert len(c.children) == 1
            assert c.of_type == LanguageEnum
            assert not c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert c.description == "The main language of the game"
            assert not c.nullable
            assert c.validator_data is not None
            assert not c.validator_data.has_rules
            assert c.validator_data.has_type_check
            assert c.validator_data.of_type == LanguageEnum
            assert c.validator_data.rules is None
            assert c.type_specific is not None
            assert c.type_specific == {"choices": [1, 2, 3, 4, 5]}
            # choices type
            assert isinstance(c.children[0], Skeleton)
            assert c.children[0].children is None
            assert c.children[0].of_type == int
            assert not c.children[0].is_model
            assert not c.children[0].is_field
            assert not c.children[0].has_default_value
        if c.name == "awesome_city":
            assert isinstance(c, ComplexSkeleton)
            assert len(c.children) == 2
            assert c.of_type == City
            assert c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert c.description == "One awesome city built"
            assert not c.nullable
            assert c.validator_data is None
            # inner model (complex type)
            for ci in c.children:
                if ci.name == "name":
                    assert isinstance(c, ComplexSkeleton)
                    assert ci.children is None
                    assert ci.of_type == str
                    assert not ci.is_model
                    assert ci.is_field
                    assert not ci.has_default_value
                    assert ci.description == "The city name"
                    assert not ci.nullable
                    assert ci.validator_data is not None
                    assert not ci.validator_data.has_rules
                    assert ci.validator_data.has_type_check
                    assert ci.validator_data.of_type == str
                    assert ci.validator_data.rules is None
                if ci.name == "region":
                    assert isinstance(ci, ComplexSkeleton)
                    assert len(ci.children) == 1
                    assert ci.of_type == CityRegionEnum
                    assert not ci.is_model
                    assert ci.is_field
                    assert ci.has_default_value
                    assert ci.default == CityRegionEnum.TEMPERATE
                    assert ci.description == "The region this city is located"
                    assert ci.nullable
                    assert ci.validator_data is not None
                    assert not ci.validator_data.has_rules
                    assert ci.validator_data.has_type_check
                    assert ci.validator_data.of_type == CityRegionEnum
                    assert ci.validator_data.rules is None
                    assert ci.type_specific is not None
                    assert ci.type_specific == {
                        "choices": ["TROPICAL", "TEMPERATE", "BOREAL"]
                    }
                    # choices type
                    assert isinstance(ci.children[0], Skeleton)
                    assert ci.children[0].children is None
                    assert ci.children[0].of_type == str
                    assert not ci.children[0].is_model
                    assert not ci.children[0].is_field
                    assert not ci.children[0].has_default_value
        if c.name == "remarkable_resources":
            assert isinstance(c, ComplexSkeleton)
            assert len(c.children) == 2
            assert c.of_type == t.Union[Player, City]
            assert not c.is_model
            assert c.is_field
            assert not c.has_default_value
            assert (
                c.description
                == "Some remarkable resources of this game over the internet"
            )
            assert not c.nullable
            assert c.validator_data is not None
            assert not c.validator_data.has_rules
            assert c.validator_data.has_type_check
            assert c.validator_data.of_type == (Player, City)
            assert c.validator_data.rules is None
            # inner models (union of complex type)
            for ci in c.children:
                assert ci.of_type in (Player, City)
                assert isinstance(c, ComplexSkeleton)
                assert len(ci.children) > 0
                assert ci.is_model
                assert ci.is_field
                assert ci.description is not None
