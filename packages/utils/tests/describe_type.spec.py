from lacus.utils import describe_type


def describe_describe_type():
    def describe_when_given_none():
        def it_returns_none_type():
            assert describe_type(None) == "NoneType"

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

    def describe_when_given_a_dict():
        def it_returns_dict_for_a_non_empty_dict():
            assert describe_type({"key": "value"}) == "dict"

        def it_returns_dict_for_an_empty_dict():
            assert describe_type({}) == "dict"

    def describe_when_given_a_custom_object():
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

        def it_returns_dict_array_for_a_list_of_dicts():
            assert describe_type([{}, {"a": 1}]) == "dict[]"

        def it_returns_none_type_array_for_a_list_of_none():
            assert describe_type([None]) == "NoneType[]"

    def describe_when_given_a_heterogeneous_list():
        def it_returns_union_array_for_numbers_and_strings():
            assert describe_type([1, "a", 2, "b"]) == "(number | string)[]"

        def it_returns_union_array_for_strings_numbers_and_booleans():
            assert describe_type(["hello", 42, True]) == "(string | number | boolean)[]"

        def it_returns_union_array_for_numbers_and_dicts():
            assert describe_type([1, {}, 2, {"a": 1}]) == "(number | dict)[]"

        def it_returns_union_array_for_strings_and_none_type():
            assert describe_type(["a", None, "b"]) == "(string | NoneType)[]"

    def describe_when_given_a_tuple():
        def it_returns_tuple_empty_for_an_empty_tuple():
            assert describe_type(()) == "tuple (empty)"

        def it_returns_number_tuple_for_a_homogeneous_tuple():
            assert describe_type((1, 2, 3)) == "number tuple"

        def it_returns_union_tuple_for_a_heterogeneous_tuple():
            assert describe_type((1, "a")) == "(number | string) tuple"

        def it_returns_none_type_tuple_for_a_single_none():
            assert describe_type((None,)) == "NoneType tuple"

    def describe_when_given_python_builtin_types():
        def it_returns_set_for_a_set():
            assert describe_type({1}) == "set"

        def it_returns_frozenset_for_a_frozenset():
            assert describe_type(frozenset()) == "frozenset"

        def it_returns_bytes_for_bytes():
            assert describe_type(b"abc") == "bytes"

        def it_returns_bytearray_for_bytearray():
            assert describe_type(bytearray(b"abc")) == "bytearray"

        def it_returns_complex_number_for_complex():
            assert describe_type(1 + 2j) == "complex number"

        def it_returns_function_for_a_lambda():
            assert describe_type(lambda: None) == "function"

        def it_returns_type_for_a_class():
            assert describe_type(int) == "type"

    def describe_python_specific_cases():
        def it_treats_bool_as_boolean_not_integer():
            assert describe_type(True) == "boolean"
            assert describe_type(False) == "boolean"

        def it_treats_none_in_a_list_as_none_type():
            assert describe_type([None, None]) == "NoneType[]"

        def it_treats_mixed_int_and_float_in_list_as_number():
            assert describe_type([1, 1.5]) == "number[]"
