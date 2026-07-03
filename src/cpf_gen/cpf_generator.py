"""Generator for CPF (Cadastro de Pessoa Física) identifiers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cpf_dv import CpfCheckDigits
from cpf_dv.exceptions import CpfCheckDigitsException
from lacus.utils import generate_random_sequence

from .cpf_generator_options import CPF_PREFIX_MAX_LENGTH, CpfGeneratorOptions

if TYPE_CHECKING:
    from .types import CpfGeneratorOptionsInput


def _format_cpf(raw: str) -> str:
    return f"{raw[:3]}.{raw[3:6]}.{raw[6:9]}-{raw[9:11]}"


class CpfGenerator:
    """Generator for CPF identifiers.

    Builds valid 11-digit CPF values by combining an optional ``prefix`` with a
    randomly generated sequence and computed check digits. Options control
    ``prefix`` and whether the result is formatted (``000.000.000-00``).
    """

    __slots__ = ("_options",)

    def __init__(
        self,
        options: CpfGeneratorOptionsInput | None = None,
        *,
        format: bool | None = None,
        prefix: str | None = None,
    ) -> None:
        """Create a new :class:`CpfGenerator` with optional defaults.

        Default options apply to every call to :meth:`generate` unless
        overridden by the per-call ``options`` argument. Options control
        ``prefix`` and whether the generated CPF is formatted.

        When ``options`` is a :class:`CpfGeneratorOptions` instance, that
        instance is used directly (no copy is created). Mutating it later (e.g.
        via the :attr:`options` property or the original reference) affects
        future :meth:`generate` calls that do not pass per-call options. When a
        plain mapping or ``None`` is passed, a new :class:`CpfGeneratorOptions`
        instance is created from it.

        Raises:
            ``CpfGeneratorOptionsTypeError``: If any option has an invalid
                type.
            ``CpfGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of digits.
        """
        if isinstance(options, CpfGeneratorOptions):
            self._options = options
        else:
            self._options = CpfGeneratorOptions(
                options,
                format=format,
                prefix=prefix,
            )

    @property
    def options(self) -> CpfGeneratorOptions:
        """Return default options used when per-call options are omitted.

        The returned object is the same instance used internally; mutating it
        (e.g. via setters on :class:`CpfGeneratorOptions`) affects future
        :meth:`generate` calls that do not pass ``options``.
        """
        return self._options

    def generate(
        self,
        options: CpfGeneratorOptionsInput | None = None,
        *,
        format: bool | None = None,
        prefix: str | None = None,
    ) -> str:
        """Generate a valid CPF value.

        Builds an 11-digit CPF from the configured ``prefix`` (if any), a
        random sequence of digits, and two computed check digits. If
        ``format`` is enabled, the result is returned as
        ``000.000.000-00``.

        Per-call options are merged over the instance default options for this call only; the instance defaults are unchanged.

        Raises:
            ``CpfGeneratorOptionsTypeError``: If any option has an invalid
                type.
            ``CpfGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of digits.
        """
        if options is None and format is None and prefix is None:
            actual_options = self._options
        else:
            actual_options = self._merge_options(options, format, prefix)

        digits_to_generate = CPF_PREFIX_MAX_LENGTH - len(actual_options.prefix)
        generated_cpf = actual_options.prefix + generate_random_sequence(
            digits_to_generate,
            "numeric",
        )

        try:
            generated_cpf = CpfCheckDigits(generated_cpf).cpf
        except CpfCheckDigitsException:
            return self.generate(options, format=format, prefix=prefix)

        if actual_options.format:
            return _format_cpf(generated_cpf)

        return generated_cpf

    def _merge_options(
        self,
        options: CpfGeneratorOptionsInput | None,
        format: bool | None,
        prefix: str | None,
    ) -> CpfGeneratorOptions:
        layers: list[CpfGeneratorOptionsInput | dict[str, Any]] = [self._options]

        if options is not None:
            layers.append(options)

        kwargs: dict[str, Any] = {}

        if format is not None:
            kwargs["format"] = format
        if prefix is not None:
            kwargs["prefix"] = prefix
        if kwargs:
            layers.append(kwargs)

        return CpfGeneratorOptions(*layers)


__all__ = ["CpfGenerator"]
