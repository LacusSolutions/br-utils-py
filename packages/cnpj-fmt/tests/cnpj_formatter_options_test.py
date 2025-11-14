import pytest
from cnpj_fmt import CnpjFormatterOptions


class TestCnpjFormatterOptions:
    def test_constructor_with_all_no_params(self):
        options = CnpjFormatterOptions()
        assert options.is_escaped() is False
        assert options.is_hidden() is False
        assert options.get_hidden_key() == "*"
        assert options.get_hidden_start() == 5
        assert options.get_hidden_end() == 13
        assert options.get_dot_key() == "."
        assert options.get_slash_key() == "/"
        assert options.get_dash_key() == "-"
        assert callable(options.get_on_fail())

    def test_constructor_with_all_none_params(self):
        options = CnpjFormatterOptions(
            escape=None,
            hidden=None,
            hidden_key=None,
            hidden_start=None,
            hidden_end=None,
            dot_key=None,
            slash_key=None,
            dash_key=None,
            on_fail=None,
        )

        assert options.is_escaped() is False
        assert options.is_hidden() is False
        assert options.get_hidden_key() == "*"
        assert options.get_hidden_start() == 5
        assert options.get_hidden_end() == 13
        assert options.get_dot_key() == "."
        assert options.get_slash_key() == "/"
        assert options.get_dash_key() == "-"
        assert callable(options.get_on_fail())

    def test_constructor_with_all_params(self):
        def on_fail_callback(value: str) -> str:
            return f"ERROR: {value}"

        options = CnpjFormatterOptions(
            escape=True,
            hidden=True,
            hidden_key="#",
            hidden_start=1,
            hidden_end=8,
            dot_key="|",
            slash_key="_",
            dash_key="~",
            on_fail=on_fail_callback,
        )

        assert options.is_escaped() is True
        assert options.is_hidden() is True
        assert options.get_hidden_key() == "#"
        assert options.get_hidden_start() == 1
        assert options.get_hidden_end() == 8
        assert options.get_dot_key() == "|"
        assert options.get_slash_key() == "_"
        assert options.get_dash_key() == "~"
        assert options.get_on_fail() is on_fail_callback

    def test_merge_with_partial_overrides(self):
        original_options = CnpjFormatterOptions(
            escape=False,
            hidden=False,
            hidden_key="*",
            hidden_start=3,
            hidden_end=10,
            dot_key=".",
            slash_key="/",
            dash_key="-",
        )
        merged_options = original_options.merge(
            escape=True,
            hidden=None,
            hidden_key="#",
            hidden_start=None,
            hidden_end=None,
            dot_key="_",
            slash_key="|",
            dash_key=None,
        )

        assert merged_options.is_escaped() is True
        assert merged_options.is_hidden() is False
        assert merged_options.get_hidden_key() == "#"
        assert merged_options.get_hidden_start() == 3
        assert merged_options.get_hidden_end() == 10
        assert merged_options.get_dot_key() == "_"
        assert merged_options.get_slash_key() == "|"
        assert merged_options.get_dash_key() == "-"

    def test_set_escape(self):
        options = CnpjFormatterOptions()
        options.set_escape(True)

        assert options.is_escaped() is True

        options.set_escape(False)

        assert options.is_escaped() is False

    def test_set_hide(self):
        options = CnpjFormatterOptions()
        options.set_hide(True)

        assert options.is_hidden() is True

        options.set_hide(False)

        assert options.is_hidden() is False

    def test_set_hidden_key(self):
        options = CnpjFormatterOptions()
        options.set_hidden_key("X")

        assert options.get_hidden_key() == "X"

        options.set_hidden_key("?")

        assert options.get_hidden_key() == "?"

    def test_set_hidden_range_with_valid_values(self):
        options = CnpjFormatterOptions()
        options.set_hidden_range(0, 10)

        assert options.get_hidden_start() == 0
        assert options.get_hidden_end() == 10

        options.set_hidden_range(5, 7)

        assert options.get_hidden_start() == 5
        assert options.get_hidden_end() == 7

    def test_set_hidden_range_with_swapped_values(self):
        options = CnpjFormatterOptions()
        options.set_hidden_range(8, 2)

        assert options.get_hidden_start() == 2
        assert options.get_hidden_end() == 8

    def test_set_hidden_range_with_invalid_start(self):
        options = CnpjFormatterOptions()

        with pytest.raises(
            ValueError,
            match='Option "hiddenStart" must be an integer between 0 and 13.',
        ):
            options.set_hidden_range(-1, 5)

    def test_set_hidden_range_with_invalid_end(self):
        options = CnpjFormatterOptions()

        with pytest.raises(
            ValueError,
            match='Option "hiddenRange.end" must be an integer between 0 and 13.',
        ):
            options.set_hidden_range(5, 14)

    def test_set_hidden_range_with_start_too_high(self):
        options = CnpjFormatterOptions()

        with pytest.raises(
            ValueError,
            match='Option "hiddenStart" must be an integer between 0 and 13.',
        ):
            options.set_hidden_range(14, 5)

    def test_set_dot_key(self):
        options = CnpjFormatterOptions()
        options.set_dot_key("|")

        assert options.get_dot_key() == "|"

        options.set_dot_key(" ")

        assert options.get_dot_key() == " "

    def test_set_slash_key(self):
        options = CnpjFormatterOptions()
        options.set_slash_key("|")

        assert options.get_slash_key() == "|"

        options.set_slash_key("@")

        assert options.get_slash_key() == "@"

    def test_set_dash_key(self):
        options = CnpjFormatterOptions()
        options.set_dash_key("~")

        assert options.get_dash_key() == "~"

        options.set_dash_key("_")

        assert options.get_dash_key() == "_"

    def test_set_on_fail_with_valid_callback(self):
        options = CnpjFormatterOptions()

        def callback(value: str) -> str:
            return f"ERROR: {value}"

        options.set_on_fail(callback)

        assert options.get_on_fail() is callback

    def test_set_on_fail_with_invalid_callback(self):
        options = CnpjFormatterOptions()

        with pytest.raises(TypeError):
            options.set_on_fail("not a callback")

    def test_set_on_fail_with_array(self):
        options = CnpjFormatterOptions()

        with pytest.raises(TypeError):
            options.set_on_fail(["not", "callable"])

    def test_set_on_fail_with_none(self):
        options = CnpjFormatterOptions()

        with pytest.raises(TypeError):
            options.set_on_fail(None)

    def test_set_on_fail_with_int(self):
        options = CnpjFormatterOptions()

        with pytest.raises(TypeError):
            options.set_on_fail(123)

    def test_boundary_values_for_hidden_range(self):
        options = CnpjFormatterOptions()
        options.set_hidden_range(0, 0)

        assert options.get_hidden_start() == 0
        assert options.get_hidden_end() == 0

        options.set_hidden_range(10, 10)

        assert options.get_hidden_start() == 10
        assert options.get_hidden_end() == 10

    def test_default_on_fail_callback_behavior(self):
        options = CnpjFormatterOptions()
        callback = options.get_on_fail()
        result = callback("test input")

        assert result == "test input"

    def test_merge_returns_new_instance(self):
        original_options = CnpjFormatterOptions(
            None, None, None, None, None, None, None, None
        )
        merged_options = original_options.merge(
            None, None, None, None, None, None, None, None
        )

        assert original_options is not merged_options
        assert isinstance(merged_options, CnpjFormatterOptions)

    def test_merge_with_all_nones_preserves_original_values(self):
        def on_fail_callback(value: str) -> str:
            return f"ERROR: {value}"

        original_options = CnpjFormatterOptions(
            escape=True,
            hidden=True,
            hidden_key="#",
            hidden_start=1,
            hidden_end=8,
            dot_key="|",
            slash_key="@",
            dash_key="~",
            on_fail=on_fail_callback,
        )
        merged_options = original_options.merge(
            None, None, None, None, None, None, None, None
        )

        assert merged_options.is_escaped() is True
        assert merged_options.is_hidden() is True
        assert merged_options.get_hidden_key() == "#"
        assert merged_options.get_hidden_start() == 1
        assert merged_options.get_hidden_end() == 8
        assert merged_options.get_dot_key() == "|"
        assert merged_options.get_slash_key() == "@"
        assert merged_options.get_dash_key() == "~"

    def test_constructor_with_mixed_none_and_valid_values(self):
        def on_fail_callback(value: str) -> str:
            return f"CUSTOM: {value}"

        options = CnpjFormatterOptions(
            escape=True,
            hidden=None,
            hidden_key=None,
            hidden_start=4,
            hidden_end=None,
            dot_key=None,
            slash_key=None,
            dash_key="~",
            on_fail=on_fail_callback,
        )

        assert options.is_escaped() is True
        assert options.is_hidden() is False
        assert options.get_hidden_key() == "*"
        assert options.get_hidden_start() == 4
        assert options.get_hidden_end() == 13
        assert options.get_dot_key() == "."
        assert options.get_slash_key() == "/"
        assert options.get_dash_key() == "~"
        assert options.get_on_fail() is on_fail_callback
