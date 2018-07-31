import enum
import typing as t

import middle

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


def test_complex_model():

    skel = translate(Game)

    assert isinstance(skel, Skeleton)
    assert len(skel.children) == 10
    assert skel.type == Game
    assert not skel.has_default_value
    assert skel.name == "Game"
    assert skel.description == "An electronic game model"
    assert not skel.nullable
    assert skel.validator_data is None

    for c in skel.children:

        # ------------------------------------------------------------------- #
        # name field
        # ------------------------------------------------------------------- #
        if c.name == "name":
            assert isinstance(c, Skeleton)
            assert c.children is None
            assert c.type == str
            assert not c.has_default_value
            assert c.description == "The name of the game"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.rules is None
            assert c.validator_data.type_check == str

        # ------------------------------------------------------------------- #
        # platform field
        # ------------------------------------------------------------------- #
        if c.name == "platform":
            assert isinstance(c, Skeleton)
            assert len(c.children) == 1
            assert c.type == PlatformEnum
            assert not c.has_default_value
            assert c.description == "Which platform it runs on"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.rules is None
            assert c.validator_data.type_check == PlatformEnum
            assert c.type_specific is not None
            assert c.type_specific == {
                "choices": ["XBOX1", "PLAYSTATION4", "PC"]
            }
            # choices type
            assert isinstance(c.children[0], Skeleton)
            assert c.children[0].children is None
            assert c.children[0].type == str
            assert not c.children[0].has_default_value
            assert c.children[0].validator_data is None
            assert c.children[0].name is None
            assert c.children[0].type_specific is None
            assert c.children[0].description is None
            assert c.children[0].nullable is False

        # ------------------------------------------------------------------- #
        # score field
        # ------------------------------------------------------------------- #
        if c.name == "score":
            assert isinstance(c, Skeleton)
            assert c.children is None
            assert c.type == float
            assert not c.has_default_value
            assert c.description == "The average score of the game"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.type_check == float
            assert c.validator_data.rules == {
                "minimum": 0,
                "maximum": 10,
                "multiple_of": 0.1,
            }

        # ------------------------------------------------------------------- #
        # resolution_tested field
        # ------------------------------------------------------------------- #
        if c.name == "resolution_tested":
            assert isinstance(c, Skeleton)
            assert c.children is None
            assert c.type == str
            assert not c.has_default_value
            assert c.description == "The resolution which the game was tested"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.rules == {"pattern": "^\d+x\d+$"}
            assert c.validator_data.type_check == str

        # ------------------------------------------------------------------- #
        # genre field
        # ------------------------------------------------------------------- #
        if c.name == "genre":
            assert isinstance(c, Skeleton)
            assert len(c.children) == 1
            assert c.type == t.List[str]
            assert not c.has_default_value
            assert c.description == "One or more genres this game is part of"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.type_check == list
            assert c.validator_data.rules == {
                "min_items": 1,
                "unique_items": True,
            }
            # inner list type
            assert isinstance(c.children[0], Skeleton)
            assert c.children[0].children is None
            assert c.children[0].type == str
            assert not c.children[0].has_default_value
            assert c.children[0].validator_data is None
            assert c.children[0].name is None
            assert c.children[0].type_specific is None
            assert c.children[0].description is None
            assert c.children[0].nullable is False

        # ------------------------------------------------------------------- #
        # rating field
        # ------------------------------------------------------------------- #
        if c.name == "rating":
            assert isinstance(c, Skeleton)
            assert len(c.children) == 1
            assert c.type == t.Dict[str, float]
            assert not c.has_default_value
            assert c.description == "Ratings given on specialized websites"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.type_check == dict
            assert c.validator_data.rules == {"min_properties": 3}
            # inner dict type
            assert isinstance(c.children[0], Skeleton)
            assert c.children[0].children is None
            assert c.children[0].type == float
            assert not c.children[0].has_default_value
            assert c.children[0].validator_data is None
            assert c.children[0].name is None
            assert c.children[0].type_specific is None
            assert c.children[0].description is None
            assert c.children[0].nullable is False

        # ------------------------------------------------------------------- #
        # players field
        # ------------------------------------------------------------------- #
        if c.name == "players":
            assert isinstance(c, Skeleton)
            assert len(c.children) == 1
            assert c.type == t.Set[Player]
            assert not c.has_default_value
            assert (
                c.description == "Some of the notorious players of this game"
            )
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.rules is None
            assert c.validator_data.type_check == set
            # inner set type
            ci = c.children[0]
            assert isinstance(ci, Skeleton)
            assert len(ci.children) == 2
            assert ci.type == Player
            assert not ci.has_default_value
            assert ci.validator_data is None
            assert ci.name == "Player"
            assert ci.type_specific is None
            assert ci.description is None
            assert ci.nullable is False
            # inner model (complex type)
            for cj in ci.children:
                if cj.name == "nickname":
                    assert isinstance(c, Skeleton)
                    assert cj.children is None
                    assert cj.type == str
                    assert not cj.has_default_value
                    assert (
                        cj.description
                        == "The nickname of the player over the internet"
                    )
                    assert not cj.nullable
                    assert cj.validator_data is not None
                    assert cj.validator_data.type_check == str
                    assert cj.validator_data.rules is None
                if cj.name == "youtube_channel":
                    assert isinstance(c, Skeleton)
                    assert cj.children is None
                    assert cj.type == str
                    assert cj.has_default_value
                    assert cj.default_value is None
                    assert (
                        cj.description == "The YouTube channel of the player"
                    )
                    assert not cj.nullable
                    assert cj.validator_data is not None
                    assert cj.validator_data.type_check == (
                        str,
                        middle.compat.NoneType,
                    )
                    assert cj.validator_data.rules is None

        # ------------------------------------------------------------------- #
        # language field
        # ------------------------------------------------------------------- #
        if c.name == "language":
            assert isinstance(c, Skeleton)
            assert len(c.children) == 1
            assert c.type == LanguageEnum
            assert not c.has_default_value
            assert c.description == "The main language of the game"
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.type_check == LanguageEnum
            assert c.validator_data.rules is None
            assert c.type_specific is not None
            assert c.type_specific == {"choices": [1, 2, 3, 4, 5]}
            # choices type
            assert isinstance(c.children[0], Skeleton)
            assert c.children[0].children is None
            assert c.children[0].type == int
            assert not c.children[0].has_default_value
            assert c.children[0].validator_data is None
            assert c.children[0].name is None
            assert c.children[0].type_specific is None
            assert c.children[0].description is None
            assert c.children[0].nullable is False

        # ------------------------------------------------------------------- #
        # awesome city field
        # ------------------------------------------------------------------- #
        if c.name == "awesome_city":
            assert isinstance(c, Skeleton)
            assert len(c.children) == 2
            assert c.type == City
            assert not c.has_default_value
            assert c.description == "One awesome city built"
            assert not c.nullable
            assert c.validator_data is None
            # inner model (complex type)
            for ci in c.children:
                if ci.name == "name":
                    assert isinstance(c, Skeleton)
                    assert ci.children is None
                    assert ci.type == str
                    assert not ci.has_default_value
                    assert ci.description == "The city name"
                    assert not ci.nullable
                    assert ci.validator_data is not None
                    assert ci.validator_data.type_check == str
                    assert ci.validator_data.rules is None
                if ci.name == "region":
                    assert isinstance(ci, Skeleton)
                    assert len(ci.children) == 1
                    assert ci.type == CityRegionEnum
                    assert ci.has_default_value
                    assert ci.default_value == CityRegionEnum.TEMPERATE
                    assert ci.description == "The region this city is located"
                    assert not ci.nullable
                    assert ci.validator_data is not None
                    assert ci.validator_data.type_check == CityRegionEnum
                    assert ci.validator_data.rules is None
                    assert ci.type_specific is not None
                    assert ci.type_specific == {
                        "choices": ["TROPICAL", "TEMPERATE", "BOREAL"]
                    }
                    # choices type
                    assert isinstance(ci.children[0], Skeleton)
                    assert ci.children[0].children is None
                    assert ci.children[0].type == str
                    assert not ci.children[0].has_default_value
                    assert ci.children[0].validator_data is None
                    assert ci.children[0].name is None
                    assert ci.children[0].type_specific is None
                    assert ci.children[0].description is None
                    assert ci.children[0].nullable is False

        # ------------------------------------------------------------------- #
        # remarkable_resources field
        # ------------------------------------------------------------------- #
        if c.name == "remarkable_resources":
            assert isinstance(c, Skeleton)
            assert len(c.children) == 2
            assert c.type == t.Union[Player, City]
            assert not c.has_default_value
            assert (
                c.description
                == "Some remarkable resources of this game over the internet"
            )
            assert not c.nullable
            assert c.validator_data is not None
            assert c.validator_data.type_check == (Player, City)
            assert c.validator_data.rules is None
            # inner models (union of complex type)
            for ci in c.children:
                assert ci.type in (Player, City)
                assert isinstance(c, Skeleton)
                assert len(ci.children) > 0
                assert ci.name is not None
