"""Behavioral spec for ``cnpj_fmt``.

Combines the shared cases of the JavaScript reference suite
(``js/packages/cnpj-fmt/tests/cnpj-fmt.spec.ts``) and the PHP reference suite
(``php/packages/cnpj-fmt/tests/specs/cnpj-fmt.spec.php``), following the
business rules documented in ``AGENTS.md``.

Dropped from the JS suite: the ``spyOn(CnpjFormatter.prototype, 'format')`` test
(delegation is asserted via behavioral parity with ``CnpjFormatter.format``,
matching the PHP approach).
"""

from cnpj_fmt import CnpjFormatter, CnpjFormatterOptions, cnpj_fmt


def describe_cnpj_fmt():
    def describe_when_called():
        def it_matches_cnpj_formatter_format_behavior():
            input_value = "91415732000793"
            formatter = CnpjFormatter()

            assert cnpj_fmt(input_value) == formatter.format(input_value)

        def it_accepts_options_and_forwards_formatting_behavior():
            input_value = "01ABC234000X56"
            options = {"slash_key": "|"}

            assert cnpj_fmt(input_value, options) == "01.ABC.234|000X-56"

    def describe_when_called_with_named_options():
        input_value = "12ABC34500DE99"
        default_hidden_length = (
            CnpjFormatterOptions.DEFAULT_HIDDEN_END
            - CnpjFormatterOptions.DEFAULT_HIDDEN_START
            + 1
        )

        def it_forwards_hidden_to_the_formatter():
            assert cnpj_fmt(input_value, hidden=True) == CnpjFormatter(
                hidden=True
            ).format(input_value)

            assert (
                cnpj_fmt(input_value, hidden=True).count("*") == default_hidden_length
            )

        def it_forwards_encode_to_the_formatter():
            assert cnpj_fmt(input_value, encode=True) == CnpjFormatter(
                encode=True
            ).format(input_value)

            assert cnpj_fmt(input_value, encode=True) == "12.ABC.345%2F00DE-99"

        def it_forwards_on_fail_to_the_formatter():
            def on_fail(_value, _error):
                return "fallback"

            assert cnpj_fmt("short", on_fail=on_fail) == CnpjFormatter(
                on_fail=on_fail
            ).format("short")

        def it_combines_options_mapping_with_named_overrides():
            assert cnpj_fmt(
                input_value,
                {"slash_key": "|"},
                hidden=True,
            ) == CnpjFormatter({"slash_key": "|"}, hidden=True,).format(input_value)
