__version__ = "0.1.0"

import logging

import middle
from middle.options import MetadataOption
from middle.options import metadata_options

logging.getLogger(__name__).addHandler(logging.NullHandler())

metadata_options.append(MetadataOption(name="description", type_=str))

middle.config.add_option("openapi_model_as_component", bool, True)
middle.config.add_option("openapi_enum_as_component", bool, True)

__all__ = ()
