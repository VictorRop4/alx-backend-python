#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """Unit test case for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
   
   
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
     ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that access_nested_map raises KeyError with proper message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[len(nested_map) if nested_map else 0]))


class TestGetJson(unittest.TestCase):
    """Test case for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns expected JSON and calls requests.get correctly."""

        # Create a Mock object to represent the response from requests.get
        mock_response = Mock()

        # Set the mock object’s json() method to return the test_payload
        mock_response.json.return_value = test_payload

        # Set requests.get to return this mock response
        mock_get.return_value = mock_response

        # Call the actual function under test
        result = get_json(test_url)

        # Assert that requests.get was called once with the correct URL
        mock_get.assert_called_once_with(test_url)

        # Assert that the result matches the expected test_payload
        self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """Test case for the utils.memoize decorator."""

    def test_memoize(self):
        """Test that a_property is cached after first call and a_method is called only once."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()

            # Call the memoized property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Both calls should return the same result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # a_method should be called only once due to memoization
            mock_method.assert_called_once()



if __name__ == "__main__":
    unittest.main()


        
      
