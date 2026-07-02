"""Unified API for CNPJ formatting, generation, and validation."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from cnpj_fmt import CnpjFormatter, CnpjFormatterOptions
from cnpj_gen import CnpjGenerator, CnpjGeneratorOptions
from cnpj_val import CnpjValidator, CnpjValidatorOptions

if TYPE_CHECKING:
    from cnpj_fmt.types import CnpjFormatterOptionsInput
    from cnpj_fmt.types import CnpjInput as CnpjFormatterInput
    from cnpj_gen.types import CnpjGeneratorOptionsInput
    from cnpj_gen.types import CnpjType as CnpjGeneratorType
    from cnpj_val.types import CnpjInput as CnpjValidatorInput
    from cnpj_val.types import CnpjType as CnpjValidatorType
    from cnpj_val.types import CnpjValidatorOptionsInput


class CnpjUtils:
    """Unified API for CNPJ (Cadastro Nacional da Pessoa Jurídica) formatting,
    generation, and validation.

    Wraps a configurable formatter, generator, and validator so you can format,
    generate, and validate CNPJ values from a single instance.
    """

    __slots__ = ("_formatter", "_generator", "_validator")

    def __init__(
        self,
        *,
        formatter: (
            CnpjFormatter | CnpjFormatterOptions | CnpjFormatterOptionsInput | None
        ) = None,
        generator: (
            CnpjGenerator | CnpjGeneratorOptions | CnpjGeneratorOptionsInput | None
        ) = None,
        validator: (
            CnpjValidator | CnpjValidatorOptions | CnpjValidatorOptionsInput | None
        ) = None,
    ) -> None:
        """Create a new :class:`CnpjUtils` with customized options.

        Each of ``formatter``, ``generator``, and ``validator`` can be omitted
        (defaults are used), or provided as an instance,
        :class:`CnpjFormatterOptions` / :class:`CnpjGeneratorOptions` /
        :class:`CnpjValidatorOptions`, or a plain mapping of options.

        When a component instance is passed, it is used directly (same
        reference). When ``None`` is passed for a component, a new instance
        with default options is created.

        Raises:
            ``CnpjFormatterOptionsTypeError``: If formatter options have an
                invalid type.
            ``CnpjFormatterOptionsHiddenRangeInvalidException``: If formatter
                ``hidden_start`` or ``hidden_end`` are out of valid range.
            ``CnpjFormatterOptionsForbiddenKeyCharacterException``: If any
                formatter key option contains a disallowed character.
            ``CnpjGeneratorOptionsTypeError``: If generator options have an
                invalid type.
            ``CnpjGeneratorOptionPrefixInvalidException``: If generator
                ``prefix`` is invalid.
            ``CnpjGeneratorOptionTypeInvalidException``: If generator ``type``
                is not allowed.
            ``CnpjValidatorOptionsTypeError``: If validator options have an
                invalid type.
            ``CnpjValidatorOptionTypeInvalidException``: If validator ``type``
                is not allowed.
        """
        self._formatter = self._resolve_formatter(formatter)
        self._generator = self._resolve_generator(generator)
        self._validator = self._resolve_validator(validator)

    @staticmethod
    def _resolve_formatter(
        value: CnpjFormatter | CnpjFormatterOptions | CnpjFormatterOptionsInput | None,
    ) -> CnpjFormatter:
        if value is None:
            return CnpjFormatter()

        if isinstance(value, CnpjFormatter):
            return value

        if isinstance(value, (CnpjFormatterOptions, Mapping)):
            return CnpjFormatter(value)

        return value  # type: ignore[return-value]

    @staticmethod
    def _resolve_generator(
        value: CnpjGenerator | CnpjGeneratorOptions | CnpjGeneratorOptionsInput | None,
    ) -> CnpjGenerator:
        if value is None:
            return CnpjGenerator()

        if isinstance(value, CnpjGenerator):
            return value

        if isinstance(value, (CnpjGeneratorOptions, Mapping)):
            return CnpjGenerator(value)

        return value  # type: ignore[return-value]

    @staticmethod
    def _resolve_validator(
        value: CnpjValidator | CnpjValidatorOptions | CnpjValidatorOptionsInput | None,
    ) -> CnpjValidator:
        if value is None:
            return CnpjValidator()

        if isinstance(value, CnpjValidator):
            return value

        if isinstance(value, (CnpjValidatorOptions, Mapping)):
            return CnpjValidator(value)

        return value  # type: ignore[return-value]

    @property
    def formatter(self) -> CnpjFormatter:
        """Return the formatter used by this utils instance."""
        return self._formatter

    @formatter.setter
    def formatter(
        self,
        value: CnpjFormatter | CnpjFormatterOptions | CnpjFormatterOptionsInput | None,
    ) -> None:
        """Set the active formatter used by this utils instance.

        It is flexible and can handle any of these inputs:

        1. A complete new instance of :class:`CnpjFormatter`
        2. An instance of :class:`CnpjFormatterOptions`
        3. A partial mapping with options for the formatter
        4. ``None`` creates a brand new :class:`CnpjFormatter` with default
           options

        Note that this resets the formatter instance completely. Any previous
        options will be overridden. To alter only a single option or a few
        options of the existing instance, access it directly (e.g.
        ``utils.formatter.options.hidden = True``).

        Raises:
            ``CnpjFormatterOptionsTypeError``: If options have an invalid
                type.
            ``CnpjFormatterOptionsHiddenRangeInvalidException``: If
                ``hidden_start`` or ``hidden_end`` are out of valid range.
            ``CnpjFormatterOptionsForbiddenKeyCharacterException``: If any key
                option contains a disallowed character.
        """
        self._formatter = self._resolve_formatter(value)

    @property
    def generator(self) -> CnpjGenerator:
        """Return the generator used by this utils instance."""
        return self._generator

    @generator.setter
    def generator(
        self,
        value: CnpjGenerator | CnpjGeneratorOptions | CnpjGeneratorOptionsInput | None,
    ) -> None:
        """Set the active generator used by this utils instance.

        It is flexible and can handle any of these inputs:

        1. A complete new instance of :class:`CnpjGenerator`
        2. An instance of :class:`CnpjGeneratorOptions`
        3. A partial mapping with options for the generator
        4. ``None`` creates a brand new :class:`CnpjGenerator` with
           default options

        Note that this resets the generator instance completely. Any
        previous options will be overridden. To alter only a single
        option or a few options of the existing instance, access it
        directly (e.g. ``utils.generator.options.type = 'numeric'``).

        Raises:
            ``CnpjGeneratorOptionsTypeError``: If options have an invalid
                type.
            ``CnpjGeneratorOptionPrefixInvalidException``: If ``prefix`` is
                invalid.
            ``CnpjGeneratorOptionTypeInvalidException``: If ``type`` is not
                allowed.
        """
        self._generator = self._resolve_generator(value)

    @property
    def validator(self) -> CnpjValidator:
        """Return the validator used by this utils instance."""
        return self._validator

    @validator.setter
    def validator(
        self,
        value: CnpjValidator | CnpjValidatorOptions | CnpjValidatorOptionsInput | None,
    ) -> None:
        """Set the active validator used by this utils instance.

        It is flexible and can handle any of these inputs:

        1. A complete new instance of :class:`CnpjValidator`
        2. An instance of :class:`CnpjValidatorOptions`
        3. A partial mapping with options for the validator
        4. ``None`` creates a brand new :class:`CnpjValidator` with
           default options

        Note that this resets the validator instance completely. Any
        previous options will be overridden. To alter only a single
        option or a few options of the existing instance, access it
        directly (e.g. ``utils.validator.options.type = 'numeric'``).

        Raises:
            ``CnpjValidatorOptionsTypeError``: If options have an invalid
                type.
            ``CnpjValidatorOptionTypeInvalidException``: If ``type`` is not
                allowed.
        """
        self._validator = self._resolve_validator(value)

    def format(
        self,
        cnpj_input: CnpjFormatterInput,
        options: CnpjFormatterOptionsInput = None,
        *,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        slash_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        encode: bool | None = None,
        on_fail: Any | None = None,
    ) -> str:
        """Format a CNPJ value into a human-readable string.

        Normalizes and optionally masks, HTML-escapes, or URL-encodes the
        input. Delegates to the instance formatter; per-call options override
        the formatter's defaults for this call only.

        Input is normalized by stripping non-alphanumeric characters and
        converting to uppercase. If the result length is not exactly 14, the
        configured ``on_fail`` callback is invoked with the original value and
        an error; its return value is used as the result.

        When valid, the result may be further transformed according to options:

        - If ``hidden`` is ``True``, characters between ``hidden_start`` and
          ``hidden_end`` (inclusive) are replaced with ``hidden_key``.
        - If ``escape`` is ``True``, HTML special characters are escaped.
        - If ``encode`` is ``True``, the string is URL-encoded.

        Per-call ``options`` are merged over the instance default options for
        this call only; the instance defaults are unchanged.

        Raises:
            ``CnpjFormatterInputTypeError``: If the input is not a string or
                sequence of strings.
            ``CnpjFormatterOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjFormatterOptionsHiddenRangeInvalidException``: If
                ``hidden_start`` or ``hidden_end`` are out of valid range.
            ``CnpjFormatterOptionsForbiddenKeyCharacterException``: If any key
                option contains a disallowed character.
        """
        format_kwargs = _format_forward_kwargs(
            hidden=hidden,
            hidden_key=hidden_key,
            hidden_start=hidden_start,
            hidden_end=hidden_end,
            dot_key=dot_key,
            slash_key=slash_key,
            dash_key=dash_key,
            escape=escape,
            encode=encode,
            on_fail=on_fail,
        )

        formatter = self._formatter

        if options is not None:
            if format_kwargs:
                return formatter.format(cnpj_input, options, **format_kwargs)

            return formatter.format(cnpj_input, options)

        if format_kwargs:
            return formatter.format(cnpj_input, **format_kwargs)

        return formatter.format(cnpj_input)

    def generate(
        self,
        options: CnpjGeneratorOptionsInput | None = None,
        *,
        format: bool | None = None,
        prefix: str | None = None,
        type: CnpjGeneratorType | None = None,
    ) -> str:
        """Generate a valid 14-character CNPJ, optionally with a prefix and
        formatting.

        Builds a 14-character CNPJ from the configured ``prefix`` (if any), a
        random sequence of the configured character ``type``, and two computed
        check digits. If ``format`` is enabled, the result is returned as
        ``00.000.000/0000-00``.

        Delegates to the instance generator; per-call options override the
        generator's defaults for this call only.

        Raises:
            ``CnpjGeneratorOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjGeneratorOptionPrefixInvalidException``: If ``prefix`` is
                invalid.
            ``CnpjGeneratorOptionTypeInvalidException``: If ``type`` is not
                allowed.
        """
        generate_kwargs = _generate_forward_kwargs(
            format=format,
            prefix=prefix,
            type=type,
        )

        generator = self._generator

        if options is not None:
            if generate_kwargs:
                return generator.generate(options, **generate_kwargs)

            return generator.generate(options)

        if generate_kwargs:
            return generator.generate(**generate_kwargs)

        return generator.generate()

    def is_valid(
        self,
        cnpj_input: CnpjValidatorInput,
        options: CnpjValidatorOptionsInput = None,
        *,
        case_sensitive: bool | None = None,
        type: CnpjValidatorType | None = None,
    ) -> bool:
        """Return whether the given value is a valid CNPJ.

        Delegates to the instance validator; per-call options override the
        validator's defaults for this call only.

        Raises:
            ``CnpjValidatorInputTypeError``: If the input is not a string or
                sequence of strings.
            ``CnpjValidatorOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjValidatorOptionTypeInvalidException``: If the ``type`` option
                is not allowed.
        """
        validator_kwargs = _validator_forward_kwargs(
            case_sensitive=case_sensitive,
            type=type,
        )

        validator = self._validator

        if options is not None:
            if validator_kwargs:
                return validator.is_valid(
                    cnpj_input,
                    options,
                    **validator_kwargs,
                )

            return validator.is_valid(cnpj_input, options)

        if validator_kwargs:
            return validator.is_valid(cnpj_input, **validator_kwargs)

        return validator.is_valid(cnpj_input)


def _format_forward_kwargs(
    *,
    hidden: bool | None,
    hidden_key: str | None,
    hidden_start: int | None,
    hidden_end: int | None,
    dot_key: str | None,
    slash_key: str | None,
    dash_key: str | None,
    escape: bool | None,
    encode: bool | None,
    on_fail: Any | None,
) -> dict[str, Any]:
    result: dict[str, Any] = {}

    if hidden is not None:
        result["hidden"] = hidden

    if hidden_key is not None:
        result["hidden_key"] = hidden_key

    if hidden_start is not None:
        result["hidden_start"] = hidden_start

    if hidden_end is not None:
        result["hidden_end"] = hidden_end

    if dot_key is not None:
        result["dot_key"] = dot_key

    if slash_key is not None:
        result["slash_key"] = slash_key

    if dash_key is not None:
        result["dash_key"] = dash_key

    if escape is not None:
        result["escape"] = escape

    if encode is not None:
        result["encode"] = encode

    if on_fail is not None:
        result["on_fail"] = on_fail

    if not result:
        return result

    for key, value in (
        ("hidden_start", hidden_start),
        ("hidden_end", hidden_end),
        ("dot_key", dot_key),
        ("slash_key", slash_key),
        ("dash_key", dash_key),
    ):
        if key not in result:
            result[key] = value

    return result


def _generate_forward_kwargs(
    *,
    format: bool | None,
    prefix: str | None,
    type: CnpjGeneratorType | None,
) -> dict[str, Any]:
    result: dict[str, Any] = {}

    if format is not None:
        result["format"] = format

    if prefix is not None:
        result["prefix"] = prefix

    if type is not None:
        result["type"] = type

    return result


def _validator_forward_kwargs(
    *,
    case_sensitive: bool | None,
    type: CnpjValidatorType | None,
) -> dict[str, Any]:
    result: dict[str, Any] = {}

    if case_sensitive is not None:
        result["case_sensitive"] = case_sensitive

    if type is not None:
        result["type"] = type

    return result


__all__ = ["CnpjUtils"]
