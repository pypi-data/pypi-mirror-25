"""OpenAPI spec validator validators module."""
import logging

from jsonschema.validators import Draft4Validator
from jsonschema.validators import RefResolver

from openapi_spec_validator.factories import Draft4ExtendedValidatorFactory

log = logging.getLogger(__name__)


class JSONSpecValidator:
    """
    Json documents validator against a json schema.

    :param schema: schema for validation.
    :param schema_url: schema base uri.
    """

    schema_validator_class = Draft4Validator
    spec_validator_factory = Draft4ExtendedValidatorFactory

    def __init__(self, schema, schema_url='', resolver_handlers=None):
        self.schema = schema
        self.schema_url = schema_url
        self.resolver_handlers = resolver_handlers or ()

        self.schema_validator_class.check_schema(self.schema)

    @property
    def schema_resolver(self):
        return self._get_resolver(self.schema_url, self.schema)

    def validate(self, spec, spec_url=''):
        """Validates json document spec.
        :param spec: json document in the form of a list or dict.
        :param spec_url: base uri to use when creating a
            RefResolver for the passed in spec_dict.

        :return: RefResolver for spec with cached remote $refs used during
            validation.
        :rtype: :class:`jsonschema.RefResolver`
        """
        spec_resolver = self._get_resolver(spec_url, spec)

        validator_cls = self.spec_validator_factory.from_resolver(spec_resolver)

        validator_obj = validator_cls(
            self.schema, resolver=self.schema_resolver)

        validator_obj.validate(spec)

        return spec_resolver

    def validate_url(self, url):
        """Validates json document at a given URL against a json schema.

        :param url: URL of the spec.

        :return: RefResolver for spec with cached remote $refs used during
            validation.
        :rtype: :class:`jsonschema.RefResolver`
        """
        handler = self.resolver_handlers['<all_urls>']
        return self.validate(handler(url), spec_url=url)

    def _get_resolver(self, base_uri, referrer):
        return RefResolver(base_uri, referrer, handlers=self.resolver_handlers)
