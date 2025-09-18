#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

     @parameterized.expand([
        ({}, ("a",)),                  # missing key "a"
        ({"a": 1}, ("a", "b")),        # missing key "b"
    ])

    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised for invalid paths with correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Exception message should match the missing key
        self.assertEqual(str(cm.exception), repr(path[-1]))


if __name__ == "__main__":
    unittest.main()
