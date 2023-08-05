from unittest import TestCase

from fstring import fstring


class FstringTest(TestCase):
    def test_basic_string(self):
        s = fstring("Hello")

        self.assertEqual(str(s), "Hello")

    def test_single_fstring_indicator(self):
        world = "World!"
        s = fstring("Hello {world}")

        self.assertEqual(str(s), "Hello World!")

    def test_multi_fstring_indicator(self):
        x = 6
        y = 7
        result = 13
        expected_str = "6+7=13"
        actual_str = str(fstring("{x}+{y}={result}"))

        self.assertEqual(expected_str, actual_str)

    def test_dictionary_fstring(self):
        simple_dict = {'x': '5', 'y': '10'}
        expected_str = "5!=10"
        actual_str = str(fstring("{simple_dict['x']}!={simple_dict['y']}"))

        self.assertEqual(expected_str, actual_str)

    def test_class_attribute_fstring(self):
        test_object = type('TestObject', (object,), {})
        foo = test_object()
        setattr(foo, 'test', 5)
        expected_str = "foo.test=5"
        actual_str = str(fstring("foo.test={foo.test}"))

        self.assertEqual(expected_str, actual_str)

    def test_math_expr(self):
        expected_str = "4"
        actual_str = str(fstring("{2+2}"))

        self.assertEqual(expected_str, actual_str)

    def test_bool_expr(self):
        x = 5
        y = 5
        expected_str = str(True)
        actual_str = str(fstring("{x==y}"))
        self.assertEqual(expected_str, actual_str)

