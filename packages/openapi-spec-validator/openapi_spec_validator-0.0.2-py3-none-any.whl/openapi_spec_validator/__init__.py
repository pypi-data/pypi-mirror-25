# -*- coding: utf-8 -*-
from openapi_spec_validator.shortcuts import (
    validate_spec_factory, validate_spec_url_factory,
)
from openapi_spec_validator.handlers import UrlHandler
from openapi_spec_validator.schemas import get_openapi_schema
from openapi_spec_validator.factories import JSONSpecValidatorFactory

__author__ = 'Artur Maciąg'
__email__ = 'maciag.artur@gmail.com'
__version__ = '0.0.2'
__url__ = 'https://github.com/p1c2u/openapi-spec-validator'
__license__ = 'Apache License, Version 2.0'

__all__ = ['openapi_v3_validator', 'validate_spec', 'validate_spec_url']

default_handlers = {
    '<all_urls>': UrlHandler('http', 'https', 'file'),
    'http': UrlHandler('http'),
    'https': UrlHandler('https'),
    'file': UrlHandler('file'),
}
schema_v3, schema_v3_url = get_openapi_schema('3.0.0')
openapi_v3_validator_factory = JSONSpecValidatorFactory(
    schema_v3, schema_v3_url,
    resolver_handlers=default_handlers,
)
# shortcuts
validate_spec = validate_spec_factory(
    openapi_v3_validator_factory.create)
validate_spec_url = validate_spec_url_factory(
    openapi_v3_validator_factory.create, default_handlers)
