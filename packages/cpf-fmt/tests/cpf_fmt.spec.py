"""Behavioral spec for ``cpf_fmt``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cpf-fmt/tests/cpf-fmt.spec.ts``) and the PHP reference suite
(``php/packages/cpf-fmt/tests/CpfFormatterFunctionTest.php`` via
``CpfFormatterTestCases``), following the business rules documented in
``AGENTS.md``.

Dropped from the JS suite: the ``spyOn(CpfFormatter.prototype, 'format')`` test
(delegation is asserted via behavioral parity with ``CpfFormatter.format``,
matching the PHP approach).
"""

from cpf_fmt import CpfFormatter, CpfFormatterOptions, cpf_fmt


def describe_cpf_fmt():
    def describe_when_called():
        def it_matches_cpf_formatter_format_behavior():
            input_value = "12345678910"
            formatter = CpfFormatter()

            assert cpf_fmt(input_value) == formatter.format(input_value)

        def it_accepts_options_and_forwards_formatting_behavior():
            input_value = "12345678910"
            options = {"dot_key": " ", "dash_key": "_"}

            assert cpf_fmt(input_value, options) == "123 456 789_10"

    def describe_when_called_with_named_options():
        input_value = "12345678910"
        default_hidden_length = (
            CpfFormatterOptions.DEFAULT_HIDDEN_END
            - CpfFormatterOptions.DEFAULT_HIDDEN_START
            + 1
        )

        def it_forwards_hidden_to_the_formatter():
            assert cpf_fmt(input_value, hidden=True) == CpfFormatter(
                hidden=True
            ).format(input_value)

            assert cpf_fmt(input_value, hidden=True).count("*") == default_hidden_length

        def it_forwards_encode_to_the_formatter():
            assert cpf_fmt(input_value, encode=True, dash_key="/") == CpfFormatter(
                encode=True, dash_key="/"
            ).format(input_value)

            assert cpf_fmt(input_value, encode=True, dash_key="/") == "123.456.789%2F10"

        def it_forwards_on_fail_to_the_formatter():
            def on_fail(_value, _error):
                return "fallback"

            assert cpf_fmt("short", on_fail=on_fail) == CpfFormatter(
                on_fail=on_fail
            ).format("short")

        def it_combines_options_mapping_with_named_overrides():
            assert cpf_fmt(
                input_value,
                {"dot_key": " "},
                hidden=True,
            ) == CpfFormatter(
                {"dot_key": " "}, hidden=True
            ).format(input_value)
