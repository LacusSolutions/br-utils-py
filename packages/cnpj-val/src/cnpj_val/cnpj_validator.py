"""Validator for CNPJ (Cadastro Nacional da Pessoa Jurídica) identifiers."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from cnpj_dv import CnpjCheckDigits

from .cnpj_validator_options import CNPJ_LENGTH, CnpjValidatorOptions
from .exceptions import CnpjValidatorInputTypeError

if TYPE_CHECKING:
    from .types import CnpjInput, CnpjType, CnpjValidatorOptionsInput


def _delete_table(*, keep: str) -> dict[int, int | None]:
    return str.maketrans(
        "", "", "".join(chr(code) for code in range(256) if chr(code) not in keep)
    )


_ALPHANUMERIC_KEEP = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_NUMERIC_KEEP = "0123456789"
_ALPHANUMERIC_DELETE_TABLE = _delete_table(keep=_ALPHANUMERIC_KEEP)
_NUMERIC_DELETE_TABLE = _delete_table(keep=_NUMERIC_KEEP)


class CnpjValidator:
    """Validator for CNPJ (Cadastro Nacional da Pessoa Jurídica).

    Validates CNPJ strings according to the Brazilian CNPJ validation
    algorithm.
    """

    def __init__(
        self,
        default_options: CnpjValidatorOptionsInput = None,
        *,
        case_sensitive: bool | None = None,
        type: CnpjType | None = None,
    ) -> None:
        """Create a new :class:`CnpjValidator` with optional defaults.

        Default options apply to every call to :meth:`is_valid` unless
        overridden by the per-call ``options`` argument. Options control case
        sensitivity and whether the CNPJ input is alphanumeric or numeric.

        When ``default_options`` is a :class:`CnpjValidatorOptions` instance,
        that instance is used directly (no copy is created). Mutating it later
        (e.g. via the :attr:`options` property or the original reference)
        affects future :meth:`is_valid` calls that do not pass per-call
        options. When a plain mapping or nothing is passed, a new
        :class:`CnpjValidatorOptions` instance is created from it.

        Raises:
            ``CnpjValidatorOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjValidatorOptionTypeInvalidException``: If the ``type`` option
                is not one of the allowed values.
        """
        if isinstance(default_options, CnpjValidatorOptions):
            self._options = default_options
        else:
            self._options = CnpjValidatorOptions(
                default_options,
                case_sensitive=case_sensitive,
                type=type,
            )

    @property
    def options(self) -> CnpjValidatorOptions:
        """Return default options used when per-call options are omitted.

        Note that the returned object is the same instance used internally;
        mutating it (e.g. via setters on
        :class:`CnpjValidatorOptions`) affects future :meth:`is_valid` calls
        that do not pass ``options``.
        """
        return self._options

    def is_valid(
        self,
        cnpj_input: CnpjInput,
        options: CnpjValidatorOptionsInput = None,
        *,
        case_sensitive: bool | None = None,
        type: CnpjType | None = None,
    ) -> bool:
        """Validate a CNPJ input.

        Per-call ``options`` are merged over the instance default options
        for this call only; the instance defaults are unchanged.

        Raises:
            ``CnpjValidatorInputTypeError``: If the input is not a string or
                sequence of strings.
            ``CnpjValidatorOptionsTypeError``: If any option has an invalid
                type.
            ``CnpjValidatorOptionTypeInvalidException``: If the ``type`` option
                is not one of the allowed values.
        """
        if options is None and case_sensitive is None and type is None:
            actual_options = self._options
        else:
            actual_options = self._merge_options(options, case_sensitive, type)

        actual_input = self._to_string_input(cnpj_input)

        case_sensitive = actual_options.case_sensitive
        cnpj_type = actual_options.type

        working_input = actual_input if case_sensitive else actual_input.upper()

        if cnpj_type == "numeric":
            sanitized_cnpj = working_input.translate(_NUMERIC_DELETE_TABLE)
        else:
            sanitized_cnpj = working_input.translate(_ALPHANUMERIC_DELETE_TABLE)

        if len(sanitized_cnpj) != CNPJ_LENGTH:
            return False

        if (
            sanitized_cnpj[12] < "0"
            or sanitized_cnpj[12] > "9"
            or sanitized_cnpj[13] < "0"
            or sanitized_cnpj[13] > "9"
        ):
            return False

        try:
            cnpj_check_digits = CnpjCheckDigits(sanitized_cnpj)
        except Exception:
            return False

        return sanitized_cnpj == cnpj_check_digits.cnpj

    def _merge_options(
        self,
        options: CnpjValidatorOptionsInput | None,
        case_sensitive: bool | None,
        type: CnpjType | None,
    ) -> CnpjValidatorOptions:
        """Merge per-call options over instance defaults.

        Applies when any override is present.
        """
        layers: list[CnpjValidatorOptionsInput | dict[str, Any]] = [self._options]

        kwargs: dict[str, Any] = {}

        if case_sensitive is not None:
            kwargs["case_sensitive"] = case_sensitive
        if type is not None:
            kwargs["type"] = type
        if kwargs:
            layers.append(kwargs)

        if options is not None:
            layers.append(options)

        return CnpjValidatorOptions(*layers)

    def _to_string_input(self, cnpj_input: Any) -> str:
        """Normalize the input to a string.

        Raises:
            ``CnpjValidatorInputTypeError``: If the input is not a string or
                sequence of strings.
        """
        if isinstance(cnpj_input, str):
            return cnpj_input

        if isinstance(cnpj_input, Sequence) and not isinstance(cnpj_input, str):
            for item in cnpj_input:
                if not isinstance(item, str):
                    raise CnpjValidatorInputTypeError(
                        cnpj_input,
                        "string or string[]",
                    )

            return "".join(cnpj_input)

        raise CnpjValidatorInputTypeError(cnpj_input, "string or string[]")


__all__ = ["CNPJ_LENGTH", "CnpjValidator"]
