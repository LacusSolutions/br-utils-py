from lacus.utils import describe_type


def describe_describe_type():
    def describe_when_given_none():
        def it_returns_null():
            assert describe_type(None) == "null"

    def describe_when_given_a_string():
        def it_returns_string_for_a_non_empty_string():
            assert describe_type("hello") == "string"

        def it_returns_string_for_an_empty_string():
            assert describe_type("") == "string"

        def it_returns_string_for_a_string_with_whitespace():
            assert describe_type("   ") == "string"

    def describe_when_given_a_boolean():
        def it_returns_boolean_for_true():
            assert describe_type(True) == "boolean"

        def it_returns_boolean_for_false():
            assert describe_type(False) == "boolean"

    def describe_when_given_an_integer():
        def it_returns_integer_number_for_a_positive_integer():
            assert describe_type(42) == "integer number"

        def it_returns_integer_number_for_a_negative_integer():
            assert describe_type(-42) == "integer number"

        def it_returns_integer_number_for_zero():
            assert describe_type(0) == "integer number"

    def describe_when_given_a_float():
        def it_returns_float_number_for_a_positive_float():
            assert describe_type(3.14) == "float number"

        def it_returns_float_number_for_a_negative_float():
            assert describe_type(-3.14) == "float number"

        def it_returns_nan_for_nan():
            assert describe_type(float("nan")) == "NaN"

        def it_returns_infinity_for_positive_infinity():
            assert describe_type(float("inf")) == "Infinity"

        def it_returns_infinity_for_negative_infinity():
            assert describe_type(float("-inf")) == "Infinity"

    def describe_when_given_a_non_list_object():
        def it_returns_object_for_a_dict():
            assert describe_type({"key": "value"}) == "object"

        def it_returns_object_for_an_empty_dict():
            assert describe_type({}) == "object"

        def it_returns_object_for_a_custom_object():
            class Foo:
                pass

            assert describe_type(Foo()) == "object"

    def describe_when_given_an_empty_list():
        def it_returns_array_empty():
            assert describe_type([]) == "Array (empty)"

    def describe_when_given_a_homogeneous_list():
        def it_returns_string_array_for_a_list_of_strings():
            assert describe_type(["a", "b", "c"]) == "string[]"

        def it_returns_number_array_for_a_list_of_integers():
            assert describe_type([1, 2, 3]) == "number[]"

        def it_returns_number_array_for_a_list_of_floats():
            assert describe_type([1.1, 2.2, 3.3]) == "number[]"

        def it_returns_boolean_array_for_a_list_of_booleans():
            assert describe_type([True, False, True]) == "boolean[]"

        def it_returns_object_array_for_a_list_of_dicts():
            assert describe_type([{}, {"a": 1}]) == "object[]"

    def describe_when_given_a_heterogeneous_list():
        def it_returns_union_array_for_numbers_and_strings():
            assert describe_type([1, "a", 2, "b"]) == "(number | string)[]"

        def it_returns_union_array_for_strings_numbers_and_booleans():
            assert describe_type(["hello", 42, True]) == "(string | number | boolean)[]"

        def it_returns_union_array_for_numbers_and_objects():
            assert describe_type([1, {}, 2, {"a": 1}]) == "(number | object)[]"

    def describe_python_specific_cases():
        def it_treats_bool_as_boolean_not_integer():
            assert describe_type(True) == "boolean"
            assert describe_type(False) == "boolean"

        def it_treats_none_in_a_list_as_object():
            assert describe_type([None, None]) == "object[]"

        def it_treats_mixed_int_and_float_in_list_as_number():
            assert describe_type([1, 1.5]) == "number[]"

        def it_treats_null_in_heterogeneous_list_as_object():
            assert describe_type(["a", None, "b"]) == "(string | object)[]"
