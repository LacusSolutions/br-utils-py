"""Unified API for CPF formatting, generation, and validation."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from cpf_fmt import CpfFormatter, CpfFormatterOptions
from cpf_gen import CpfGenerator, CpfGeneratorOptions
from cpf_val import CpfValidator

if TYPE_CHECKING:
    from cpf_fmt.types import CpfFormatterOptionsInput
    from cpf_fmt.types import CpfInput as CpfFormatterInput
    from cpf_gen.types import CpfGeneratorOptionsInput
    from cpf_val.types import CpfInput as CpfValidatorInput


class CpfUtils:
    """Unified API for CPF (Cadastro da Pessoa Física) formatting, generation
    and validation.

    Wraps a configurable formatter, generator, and validator so you can format,
    generate, and validate CPF values from a single instance.
    """

    __slots__ = ("_formatter", "_generator", "_validator")

    def __init__(
        self,
        *,
        formatter: (
            CpfFormatter | CpfFormatterOptions | CpfFormatterOptionsInput | None
        ) = None,
        generator: (
            CpfGenerator | CpfGeneratorOptions | CpfGeneratorOptionsInput | None
        ) = None,
        validator: CpfValidator | None = None,
    ) -> None:
        """Create a new :class:`CpfUtils` with customized options.

        Each of ``formatter``, ``generator``, and ``validator`` can be omitted
        (defaults are used), or provided as an instance,
        :class:`CpfFormatterOptions` / :class:`CpfGeneratorOptions`, or a plain
        mapping of options.

        When a component instance is passed, it is used directly (same
        reference). When ``None`` is passed for a component, a new instance
        with default options is created.

        Raises:
            ``CpfFormatterOptionsTypeError``: If formatter options have an
                invalid type.
            ``CpfFormatterOptionsHiddenRangeInvalidException``: If formatter
                ``hidden_start`` or ``hidden_end`` are out of valid range.
            ``CpfFormatterOptionsForbiddenKeyCharacterException``: If any
                formatter key option contains a disallowed character.
            ``CpfGeneratorOptionsTypeError``: If generator options have an
                invalid type.
            ``CpfGeneratorOptionPrefixInvalidException``: If generator
                ``prefix`` is invalid.
        """
        self._formatter = self._resolve_formatter(formatter)
        self._generator = self._resolve_generator(generator)
        self._validator = self._resolve_validator(validator)

    @staticmethod
    def _resolve_formatter(
        value: CpfFormatter | CpfFormatterOptions | CpfFormatterOptionsInput | None,
    ) -> CpfFormatter:
        if value is None:
            return CpfFormatter()

        if isinstance(value, CpfFormatter):
            return value

        if isinstance(value, (CpfFormatterOptions, Mapping)):
            return CpfFormatter(value)

        return value  # type: ignore[return-value]

    @staticmethod
    def _resolve_generator(
        value: CpfGenerator | CpfGeneratorOptions | CpfGeneratorOptionsInput | None,
    ) -> CpfGenerator:
        if value is None:
            return CpfGenerator()

        if isinstance(value, CpfGenerator):
            return value

        if isinstance(value, (CpfGeneratorOptions, Mapping)):
            return CpfGenerator(value)

        return value  # type: ignore[return-value]

    @staticmethod
    def _resolve_validator(value: CpfValidator | None) -> CpfValidator:
        if value is None:
            return CpfValidator()

        return value

    @property
    def formatter(self) -> CpfFormatter:
        """Return the formatter used by this utils instance."""
        return self._formatter

    @formatter.setter
    def formatter(
        self,
        value: CpfFormatter | CpfFormatterOptions | CpfFormatterOptionsInput | None,
    ) -> None:
        """Set the active formatter used by this utils instance.

        It is flexible and can handle any of these inputs:

        1. A complete new instance of :class:`CpfFormatter`
        2. An instance of :class:`CpfFormatterOptions`
        3. A partial mapping with options for the formatter
        4. ``None`` creates a brand new :class:`CpfFormatter` with default
           options

        Note that this resets the formatter instance completely. Any previous
        options will be overridden. To alter only a single option or a few
        options of the existing instance, access it directly (e.g.
        ``utils.formatter.options.hidden = True``).

        Raises:
            ``CpfFormatterOptionsTypeError``: If options have an invalid
                type.
            ``CpfFormatterOptionsHiddenRangeInvalidException``: If
                ``hidden_start`` or ``hidden_end`` are out of valid range.
            ``CpfFormatterOptionsForbiddenKeyCharacterException``: If any key
                option contains a disallowed character.
        """
        self._formatter = self._resolve_formatter(value)

    @property
    def generator(self) -> CpfGenerator:
        """Return the generator used by this utils instance."""
        return self._generator

    @generator.setter
    def generator(
        self,
        value: CpfGenerator | CpfGeneratorOptions | CpfGeneratorOptionsInput | None,
    ) -> None:
        """Set the active generator used by this utils instance.

        It is flexible and can handle any of these inputs:

        1. A complete new instance of :class:`CpfGenerator`
        2. An instance of :class:`CpfGeneratorOptions`
        3. A partial mapping with options for the generator
        4. ``None`` creates a brand new :class:`CpfGenerator` with
           default options

        Note that this resets the generator instance completely. Any
        previous options will be overridden. To alter only a single
        option or a few options of the existing instance, access it
        directly (e.g. ``utils.generator.options.format = True``).

        Raises:
            ``CpfGeneratorOptionsTypeError``: If options have an invalid
                type.
            ``CpfGeneratorOptionPrefixInvalidException``: If ``prefix`` is
                invalid.
        """
        self._generator = self._resolve_generator(value)

    @property
    def validator(self) -> CpfValidator:
        """Return the validator used by this utils instance."""
        return self._validator

    @validator.setter
    def validator(self, value: CpfValidator | None) -> None:
        """Set the active validator used by this utils instance.

        It is flexible and can handle any of these inputs:

        1. A complete new instance of :class:`CpfValidator`
        2. ``None`` creates a brand new :class:`CpfValidator`

        Note that this resets the validator instance completely.
        """
        self._validator = self._resolve_validator(value)

    def format(
        self,
        cpf_input: CpfFormatterInput,
        options: CpfFormatterOptionsInput = None,
        *,
        hidden: bool | None = None,
        hidden_key: str | None = None,
        hidden_start: int | None = None,
        hidden_end: int | None = None,
        dot_key: str | None = None,
        dash_key: str | None = None,
        escape: bool | None = None,
        encode: bool | None = None,
        on_fail: Any | None = None,
    ) -> str:
        """Format a CPF value into a human-readable string.

        Normalizes and optionally masks, HTML-escapes, or URL-encodes the
        input. Delegates to the instance formatter; per-call options override
        the formatter's defaults for this call only.

        Input is normalized by stripping non-digit characters. If the result
        length is not exactly 11, the configured ``on_fail`` callback is
        invoked with the original value and an error; its return value is
        used as the result.

        When valid, the result may be further transformed according to options:

        - If ``hidden`` is ``True``, characters between ``hidden_start`` and
          ``hidden_end`` (inclusive) are replaced with ``hidden_key``.
        - If ``escape`` is ``True``, HTML special characters are escaped.
        - If ``encode`` is ``True``, the string is URL-encoded.

        Per-call ``options`` are merged over the instance default options for
        this call only; the instance defaults are unchanged.

        Raises:
            ``CpfFormatterInputTypeError``: If the input is not a string or
                sequence of strings.
            ``CpfFormatterOptionsTypeError``: If any option has an invalid
                type.
            ``CpfFormatterOptionsHiddenRangeInvalidException``: If
                ``hidden_start`` or ``hidden_end`` are out of valid range.
            ``CpfFormatterOptionsForbiddenKeyCharacterException``: If any key
                option contains a disallowed character.
        """
        format_kwargs = _format_forward_kwargs(
            hidden=hidden,
            hidden_key=hidden_key,
            hidden_start=hidden_start,
            hidden_end=hidden_end,
            dot_key=dot_key,
            dash_key=dash_key,
            escape=escape,
            encode=encode,
            on_fail=on_fail,
        )

        formatter = self._formatter

        if options is not None:
            if format_kwargs:
                return formatter.format(cpf_input, options, **format_kwargs)

            return formatter.format(cpf_input, options)

        if format_kwargs:
            return formatter.format(cpf_input, **format_kwargs)

        return formatter.format(cpf_input)

    def generate(
        self,
        options: CpfGeneratorOptionsInput | None = None,
        *,
        format: bool | None = None,
        prefix: str | None = None,
    ) -> str:
        """Generate a valid 11-digit CPF, optionally with a prefix and
        formatting.

        Builds an 11-digit CPF from the configured ``prefix`` (if any), a
        random sequence of digits, and two computed check digits. If ``format``
        is enabled, the result is returned as ``XXX.XXX.XXX-XX``.

        Delegates to the instance generator; per-call options override the
        generator's defaults for this call only.

        Raises:
            ``CpfGeneratorOptionsTypeError``: If any option has an invalid
                type.
            ``CpfGeneratorOptionPrefixInvalidException``: If ``prefix`` is
                invalid.
        """
        generate_kwargs = _generate_forward_kwargs(format=format, prefix=prefix)

        generator = self._generator

        if options is not None:
            if generate_kwargs:
                return generator.generate(options, **generate_kwargs)

            return generator.generate(options)

        if generate_kwargs:
            return generator.generate(**generate_kwargs)

        return generator.generate()

    def is_valid(self, cpf_input: CpfValidatorInput) -> bool:
        """Return whether the given value is a valid CPF.

        Delegates to the instance validator.

        Raises:
            ``CpfValidatorInputTypeError``: If the input is not a string or
                sequence of strings.
        """
        return self._validator.is_valid(cpf_input)


def _format_forward_kwargs(
    *,
    hidden: bool | None,
    hidden_key: str | None,
    hidden_start: int | None,
    hidden_end: int | None,
    dot_key: str | None,
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
        ("dash_key", dash_key),
    ):
        if key not in result:
            result[key] = value

    return result


def _generate_forward_kwargs(
    *,
    format: bool | None,
    prefix: str | None,
) -> dict[str, Any]:
    result: dict[str, Any] = {}

    if format is not None:
        result["format"] = format

    if prefix is not None:
        result["prefix"] = prefix

    return result


__all__ = ["CpfUtils"]
