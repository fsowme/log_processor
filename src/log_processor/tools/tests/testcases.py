import jsonschema
from rest_framework.test import APITestCase as DRFAPITestCase


class APISchemaValidationMixin:
    def assertDataSchema(self, data, schema, format_checker=None):
        try:
            jsonschema.validate(data, schema, format_checker=format_checker)
        except (jsonschema.exceptions.ValidationError, jsonschema.exceptions.SchemaError) as e:
            raise AssertionError from e


class APITestCase(APISchemaValidationMixin, DRFAPITestCase):
    pass
