# coding: utf-8

"""
    Schul-Cloud Content API

"""


from __future__ import absolute_import

import os
import sys
import unittest

import schul_cloud_resources_api_v1
from schul_cloud_resources_api_v1.schema import (
    validate_resource, is_valid_resource, get_valid_examples,
    get_invalid_examples, ValidationFailed, get_schemas
)


class TestResourceSchema(unittest.TestCase):
    """ Schema unit test stubs """

    def test_there_are_valid_examples(self):
        self.assertTrue(get_valid_examples())

    def test_there_are_invalid_examples(self):
        self.assertTrue(get_invalid_examples())

    def test_valid_and_invalid_examples_are_not_the_same(self):
        for v in get_valid_examples():
            for i in get_invalid_examples():
                self.assertNotEqual(v, i, "A valid example can not be invalid.")

    def test_all_valid_examples_succeed(self):
        for v in get_valid_examples():
            self.assertTrue(is_valid_resource(v))
            validate_resource(v)

    def test_all_invalid_examples_fail(self):
        for i in get_invalid_examples():
            self.assertFalse(is_valid_resource(i))
            self.assertRaises(ValidationFailed, lambda: validate_resource(i))

class TestSchemas(unittest.TestCase):
    """ Schema unit test stubs """

    def test_there_are_schemas(self):
        for name in ["error", "search-response", "resource"]:
            self.assertTrue(name in get_schemas())

    def test_there_are_valid_examples(self):
        for schema in get_schemas().values():
            self.assertTrue(schema.get_valid_examples())

    def test_there_are_invalid_examples(self):
        for schema in get_schemas().values():
            self.assertTrue(schema.get_invalid_examples())

    def test_valid_and_invalid_examples_are_not_the_same(self):
        for schema in get_schemas().values():
            for v in schema.get_valid_examples():
                for i in schema.get_invalid_examples():
                    self.assertNotEqual(v, i, "A valid example can not be invalid.")

    def test_all_valid_examples_succeed(self):
        for schema in get_schemas().values():
            for v in schema.get_valid_examples():
                self.assertTrue(schema.is_valid(v))
                schema.validate(v)

    def test_all_invalid_examples_fail(self):
        for schema in get_schemas().values():
            for i in schema.get_invalid_examples():
                self.assertFalse(schema.is_valid(i))
                self.assertRaises(ValidationFailed, lambda: schema.validate(i))


if __name__ == '__main__':
    unittest.main()
