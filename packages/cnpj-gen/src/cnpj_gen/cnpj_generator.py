"""Generator for CNPJ (Cadastro Nacional da Pessoa Jurídica) identifiers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cnpj_dv import CnpjCheckDigits
from cnpj_dv.exceptions import CnpjCheckDigitsException
from lacus.utils import generate_random_sequence

from .cnpj_generator_options import CNPJ_PREFIX_MAX_LENGTH, CnpjGeneratorOptions

if TYPE_CHECKING:
    from .types import CnpjGeneratorOptionsInput, CnpjType


def _format_cnpj(raw: str) -> str:
    return f"{raw[:2]}.{raw[2:5]}.{raw[5:8]}/{raw[8:12]}-{raw[12:14]}"


class CnpjGenerator:
    """Generator for CNPJ identifiers.

    Builds valid 14-character CNPJ values by combining an optional
    ``prefix`` with a randomly generated sequence and computed check
    digits. Options control ``prefix``, character ``type`` (``"numeric"``,
    ``"alphabetic"``, or ``"alphanumeric"``), and whether the result is
    formatted (``00.000.000/0000-00``).
    """

    __slots__ = ("_options",)

    def __init__(
        self,
        options: CnpjGeneratorOptionsInput | None = None,
        *,
        format: bool | None = None,
        prefix: str | None = None,
        type: CnpjType | None = None,
    ) -> None:
        """Create a new :class:`CnpjGenerator` with optional defaults.

        Default options apply to every call to :meth:`generate` unless
        overridden by the per-call ``options`` argument. Options control
        ``prefix``, character ``type``, and whether the generated CNPJ
        is formatted.

        When ``options`` is a :class:`CnpjGeneratorOptions` instance,
        that instance is used directly (no copy is created). Mutating it
        later (e.g. via the :attr:`options` property or the original
        reference) affects future :meth:`generate` calls that do not pass
        per-call options. When a plain mapping or ``None`` is passed, a
        new :class:`CnpjGeneratorOptions` instance is created from it.

        Raises:
            ``CnpjGeneratorOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of characters.
            ``CnpjGeneratorOptionTypeInvalidException``: If the ``type``
                option is not one of the allowed values.
        """
        if isinstance(options, CnpjGeneratorOptions):
            self._options = options
        else:
            self._options = CnpjGeneratorOptions(
                options,
                format=format,
                prefix=prefix,
                type=type,
            )

    @property
    def options(self) -> CnpjGeneratorOptions:
        """Return default options used when per-call options are omitted.

        The returned object is the same instance used internally;
        mutating it (e.g. via setters on
        :class:`CnpjGeneratorOptions`) affects future
        :meth:`generate` calls that do not pass ``options``.
        """
        return self._options

    def generate(
        self,
        options: CnpjGeneratorOptionsInput | None = None,
        *,
        format: bool | None = None,
        prefix: str | None = None,
        type: CnpjType | None = None,
    ) -> str:
        """Generate a valid CNPJ value.

        Builds a 14-character CNPJ from the configured ``prefix`` (if any),
        a random sequence of the configured character ``type``, and two
        computed check digits. If ``format`` is enabled, the result is
        returned as ``00.000.000/0000-00``.

        Per-call options are merged over the instance default options  for
        this call only; the instance defaults are unchanged.

        Raises:
            ``CnpjGeneratorOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjGeneratorOptionPrefixInvalidException``: If the ``prefix``
                option contains an invalid combination of characters.
            ``CnpjGeneratorOptionTypeInvalidException``: If the ``type`` option
                is not one of the allowed values.
        """
        if options is None and format is None and prefix is None and type is None:
            actual_options = self._options
        else:
            actual_options = self._merge_options(options, format, prefix, type)

        characters_to_generate = CNPJ_PREFIX_MAX_LENGTH - len(actual_options.prefix)
        generated_cnpj = actual_options.prefix + generate_random_sequence(
            characters_to_generate,
            actual_options.type,
        )

        try:
            generated_cnpj = CnpjCheckDigits(generated_cnpj).cnpj
        except CnpjCheckDigitsException:
            return self.generate(options, format=format, prefix=prefix, type=type)

        if actual_options.format:
            return _format_cnpj(generated_cnpj)

        return generated_cnpj

    def _merge_options(
        self,
        options: CnpjGeneratorOptionsInput | None,
        format: bool | None,
        prefix: str | None,
        type: CnpjType | None,
    ) -> CnpjGeneratorOptions:
        layers: list[CnpjGeneratorOptionsInput | dict[str, Any]] = [self._options]

        if options is not None:
            layers.append(options)

        kwargs: dict[str, Any] = {}

        if format is not None:
            kwargs["format"] = format
        if prefix is not None:
            kwargs["prefix"] = prefix
        if type is not None:
            kwargs["type"] = type
        if kwargs:
            layers.append(kwargs)

        return CnpjGeneratorOptions(*layers)


__all__ = ["CnpjGenerator"]
