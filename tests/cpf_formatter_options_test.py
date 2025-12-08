import pytest
from cpf_fmt import (
    DEFAULT_DASH_KEY,
    DEFAULT_DOT_KEY,
    DEFAULT_ESCAPE,
    DEFAULT_HIDDEN,
    DEFAULT_HIDDEN_END,
    DEFAULT_HIDDEN_KEY,
    DEFAULT_HIDDEN_START,
    DEFAULT_ON_FAIL,
    CpfFormatterHiddenRangeError,
    CpfFormatterOptions,
)


class CpfFormatterOptionsTest:
    def test_default_options_when_constructor_is_empty(self):
        options = CpfFormatterOptions()

        assert options.hidden is DEFAULT_HIDDEN
        assert options.hidden_key == DEFAULT_HIDDEN_KEY
        assert options.hidden_start == DEFAULT_HIDDEN_START
        assert options.hidden_end == DEFAULT_HIDDEN_END
        assert options.dot_key == DEFAULT_DOT_KEY
        assert options.dash_key == DEFAULT_DASH_KEY
        assert options.escape is DEFAULT_ESCAPE
        assert options.on_fail is DEFAULT_ON_FAIL

    def test_default_options_when_constructor_is_called_with_value_none(self):
        options = CpfFormatterOptions(
            hidden=None,
            hidden_key=None,
            hidden_start=None,
            hidden_end=None,
            dot_key=None,
            dash_key=None,
            escape=None,
            on_fail=None,
        )

        assert options.hidden is DEFAULT_HIDDEN
        assert options.hidden_key == DEFAULT_HIDDEN_KEY
        assert options.hidden_start == DEFAULT_HIDDEN_START
        assert options.hidden_end == DEFAULT_HIDDEN_END
        assert options.dot_key == DEFAULT_DOT_KEY
        assert options.dash_key == DEFAULT_DASH_KEY
        assert options.escape is DEFAULT_ESCAPE
        assert options.on_fail is DEFAULT_ON_FAIL

    def test_options_persisted_when_constructor_is_called_with_all_params(self):
        def on_fail_callback(value: str) -> str:
            return f"ERROR: {value}"

        options = CpfFormatterOptions(
            hidden=True,
            hidden_key="#",
            hidden_start=1,
            hidden_end=8,
            dot_key="_",
            dash_key="~",
            escape=True,
            on_fail=on_fail_callback,
        )

        assert options.hidden is True
        assert options.hidden_key == "#"
        assert options.hidden_start == 1
        assert options.hidden_end == 8
        assert options.dot_key == "_"
        assert options.dash_key == "~"
        assert options.escape is True
        assert options.on_fail is on_fail_callback

    def test_merge_returns_new_instance(self):
        original_options = CpfFormatterOptions()
        merged_options = original_options.merge()

        assert original_options is not merged_options
        assert isinstance(merged_options, CpfFormatterOptions)

    def test_new_options_returned_on_merge_called_with_all_overrides(self):
        def on_fail_callback(value: str) -> str:
            return f"ERROR: {value}"

        options = CpfFormatterOptions()

        merged_options = options.merge(
            hidden=True,
            hidden_key="#",
            hidden_start=1,
            hidden_end=8,
            dot_key="_",
            dash_key="~",
            escape=True,
            on_fail=on_fail_callback,
        )

        assert merged_options.hidden is True
        assert merged_options.hidden_key == "#"
        assert merged_options.hidden_start == 1
        assert merged_options.hidden_end == 8
        assert merged_options.dot_key == "_"
        assert merged_options.dash_key == "~"
        assert merged_options.escape is True
        assert merged_options.on_fail is on_fail_callback

    def test_new_options_returned_on_merge_called_with_none_overrides(self):
        def on_fail_callback(value: str) -> str:
            return f"ERROR: {value}"

        options = CpfFormatterOptions(
            hidden=True,
            hidden_key="#",
            hidden_start=1,
            hidden_end=8,
            dot_key="_",
            dash_key="~",
            escape=True,
            on_fail=on_fail_callback,
        )

        merged_options = options.merge(
            hidden=None,
            hidden_key=None,
            hidden_start=None,
            hidden_end=None,
            dot_key=None,
            dash_key=None,
            escape=None,
            on_fail=None,
        )

        assert merged_options.hidden is True
        assert merged_options.hidden_key == "#"
        assert merged_options.hidden_start == 1
        assert merged_options.hidden_end == 8
        assert merged_options.dot_key == "_"
        assert merged_options.dash_key == "~"
        assert merged_options.escape is True
        assert merged_options.on_fail is on_fail_callback

    def test_new_options_returned_on_merge_called_with_partial_overrides(self):
        original_options = CpfFormatterOptions(
            hidden=True,
            hidden_key="#",
            hidden_start=7,
            hidden_end=9,
        )

        merged_options = original_options.merge(
            hidden_start=5,
            dot_key="_",
            dash_key="~",
        )

        assert merged_options.hidden is True
        assert merged_options.hidden_key == "#"
        assert merged_options.hidden_start == 5
        assert merged_options.hidden_end == 9
        assert merged_options.dot_key == "_"
        assert merged_options.dash_key == "~"

    def test_set_hide(self):
        options = CpfFormatterOptions()

        options.hidden = True
        assert options.hidden is True

        options.hidden = False
        assert options.hidden is False

    def test_set_hidden_key(self):
        options = CpfFormatterOptions()

        options.hidden_key = "X"
        assert options.hidden_key == "X"

        options.hidden_key = "?"
        assert options.hidden_key == "?"

    def test_set_hidden_range_with_valid_values(self):
        options = CpfFormatterOptions()

        options.set_hidden_range(0, 10)
        assert options.hidden_start == 0
        assert options.hidden_end == 10

        options.set_hidden_range(5, 7)
        assert options.hidden_start == 5
        assert options.hidden_end == 7

    def test_set_hidden_range_with_swapped_values(self):
        options = CpfFormatterOptions()

        options.set_hidden_range(8, 2)
        assert options.hidden_start == 2
        assert options.hidden_end == 8

    def test_set_hidden_range_with_invalid_start(self):
        options = CpfFormatterOptions()

        with pytest.raises(
            CpfFormatterHiddenRangeError,
            match=r'Option "hidden_start" must be an integer between 0 and 10\.',
        ):
            options.set_hidden_range(-1, 5)

    def test_set_hidden_range_with_invalid_end(self):
        options = CpfFormatterOptions()

        with pytest.raises(
            CpfFormatterHiddenRangeError,
            match=r'Option "hidden_end" must be an integer between 0 and 10\.',
        ):
            options.set_hidden_range(5, 11)

    def test_set_hidden_range_with_start_too_high(self):
        options = CpfFormatterOptions()

        with pytest.raises(
            CpfFormatterHiddenRangeError,
            match=r'Option "hidden_start" must be an integer between 0 and 10\.',
        ):
            options.set_hidden_range(11, 5)

    def test_boundary_values_for_hidden_range(self):
        options = CpfFormatterOptions()

        options.set_hidden_range(0, 0)
        assert options.hidden_start == 0
        assert options.hidden_end == 0

        options.set_hidden_range(10, 10)
        assert options.hidden_start == 10
        assert options.hidden_end == 10

    def test_set_dot_key(self):
        options = CpfFormatterOptions()

        options.dot_key = "_"
        assert options.dot_key == "_"

        options.dot_key = " "
        assert options.dot_key == " "

    def test_set_dash_key(self):
        options = CpfFormatterOptions()

        options.dash_key = "~"
        assert options.dash_key == "~"

        options.dash_key = "@"
        assert options.dash_key == "@"

    def test_options_updated_when_escape_is_set(self):
        options = CpfFormatterOptions()

        options.escape = True
        assert options.escape is True

        options.escape = False
        assert options.escape is False

    def test_set_on_fail_with_valid_callback(self):
        def callback(value: str) -> str:
            return f"ERROR: {value}"

        options = CpfFormatterOptions()

        options.on_fail = callback
        assert options.on_fail is callback

    def test_set_on_fail_with_invalid_callback(self):
        options = CpfFormatterOptions()

        with pytest.raises(TypeError):
            options.on_fail = "not a callback"

    def test_set_on_fail_with_array(self):
        options = CpfFormatterOptions()

        with pytest.raises(TypeError):
            options.on_fail = ["not", "callable"]

    def test_set_on_fail_with_none(self):
        options = CpfFormatterOptions()

        with pytest.raises(TypeError):
            options.on_fail = None

    def test_set_on_fail_with_int(self):
        options = CpfFormatterOptions()

        with pytest.raises(TypeError):
            options.on_fail = 123

    def test_default_on_fail_callback_behavior(self):
        options = CpfFormatterOptions()
        callback = options.on_fail
        result = callback("test input")

        assert result == "test input"
