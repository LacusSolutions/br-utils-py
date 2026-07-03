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


class CpfUtils:
    """Unified API for CPF (Cadastro de Pessoa Física) formatting,
    generation, and validation.

    Wraps a configurable formatter, generator, and validator so you can
    format, generate, and validate CPF values from a single instance.
    """

    __slots__ = ("_formatter", "_generator", "_validator")

    def __init__(
        self,
        *,
        formatter: (
            CpfFormatter | CpfFormatterOptions | CpfFormatterOptionsInput | None
        ) = None,
        generator: CpfGenerator | CpfGeneratorOptions | None = None,
        validator: CpfValidator | None = None,
    ) -> None:
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
        value: CpfGenerator | CpfGeneratorOptions | None,
    ) -> CpfGenerator:
        if value is None:
            return CpfGenerator()

        if isinstance(value, CpfGenerator):
            return value

        if isinstance(value, CpfGeneratorOptions):
            return CpfGenerator(format=value.format, prefix=value.prefix)

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
        self._formatter = self._resolve_formatter(value)

    @property
    def generator(self) -> CpfGenerator:
        """Return the generator used by this utils instance."""
        return self._generator

    @generator.setter
    def generator(self, value: CpfGenerator | CpfGeneratorOptions | None) -> None:
        self._generator = self._resolve_generator(value)

    @property
    def validator(self) -> CpfValidator:
        """Return the validator used by this utils instance."""
        return self._validator

    @validator.setter
    def validator(self, value: CpfValidator | None) -> None:
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

    def generate(self, format: bool | None = None, prefix: str | None = None) -> str:
        return self._generator.generate(format, prefix)

    def is_valid(self, cpf_string: str) -> bool:
        return self._validator.is_valid(cpf_string)


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

    return result


__all__ = ["CpfUtils"]
