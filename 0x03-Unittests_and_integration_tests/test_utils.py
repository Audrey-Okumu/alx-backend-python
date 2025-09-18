#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


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

    #  parameterized test for exception cases
    @parameterized.expand([
        ({}, ("a",)),           # missing key "a"
        ({"a": 1}, ("a", "b"))  # missing key "b"
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised for invalid paths with correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Check that the exception message matches the missing key
        self.assertEqual(str(cm.exception), repr(path[-1]))

class TestGetJson(unittest.TestCase):
    """Unit tests for utils.get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns the expected payload"""
        # Mock the response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Verify requests.get was called once with the correct URL
        mock_get.assert_called_once_with(test_url)

        # Verify output matches expected payload
        self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """Unit tests for utils.memoize"""

    def test_memoize(self):
        """Test that a_property calls a_method only once"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Patch a_method inside TestClass
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            # Call twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Both calls should return the same correct result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # a_method should only be called once because of memoization
            mock_method.assert_called_once()



if __name__ == "__main__":
    unittest.main()
