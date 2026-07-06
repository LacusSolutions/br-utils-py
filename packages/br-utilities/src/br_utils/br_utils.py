"""Unified façade for Brazilian CPF and CNPJ utilities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping

from .cnpj import (
    CnpjFormatter,
    CnpjFormatterOptions,
    CnpjGenerator,
    CnpjGeneratorOptions,
    CnpjUtils,
    CnpjValidator,
    CnpjValidatorOptions,
)
from .cpf import (
    CpfFormatter,
    CpfFormatterOptions,
    CpfGenerator,
    CpfGeneratorOptions,
    CpfUtils,
)


def _resolve_utils(
    utils_cls: type[CpfUtils] | type[CnpjUtils],
    value: CpfUtils | CnpjUtils | Mapping[str, Any] | None,
) -> CpfUtils | CnpjUtils:
    if isinstance(value, utils_cls):
        return value

    if value is None:
        return utils_cls()

    return utils_cls(**value)


class BrUtils:
    """Unified API for Brazilian-related data, like CPF (Cadastro de Pessoa
    Física) and CNPJ (Cadastro Nacional da Pessoa Jurídica).

    Provides a unified interface for formatting, generating, and validating
    data.
    """

    __slots__ = ("_cnpj", "_cpf")

    def __init__(
        self,
        *,
        cpf: CpfUtils | Mapping[str, Any] | None = None,
        cnpj: CnpjUtils | Mapping[str, Any] | None = None,
        cpf_formatter: (
            CpfFormatter | CpfFormatterOptions | Mapping[str, Any] | None
        ) = None,
        cpf_generator: (
            CpfGenerator | CpfGeneratorOptions | Mapping[str, Any] | None
        ) = None,
        cnpj_formatter: (
            CnpjFormatter | CnpjFormatterOptions | Mapping[str, Any] | None
        ) = None,
        cnpj_generator: (
            CnpjGenerator | CnpjGeneratorOptions | Mapping[str, Any] | None
        ) = None,
        cnpj_validator: (
            CnpjValidator | CnpjValidatorOptions | Mapping[str, Any] | None
        ) = None,
    ) -> None:
        """Create a new :class:`BrUtils` instance with customized options.

        All options are optional. If any option is omitted, it falls back to
        its default value.

        Each of ``cpf`` and ``cnpj`` accepts either a pre-built utils
        instance or a configuration mapping spread into the corresponding
        :class:`CpfUtils` / :class:`CnpjUtils` constructor. Within that
        mapping, each resource key (``formatter``, ``generator``, and
        ``validator`` for CNPJ) accepts either an options object or a mapping
        of option values.

        Flat ``cpf_formatter`` / ``cpf_generator`` and ``cnpj_formatter`` /
        ``cnpj_generator`` / ``cnpj_validator`` arguments are supported as a
        convenience when only individual components need customization. They
        are ignored when the corresponding ``cpf`` or ``cnpj`` argument is
        provided.

        Raises:
            ``CnpjFormatterOptionsTypeError``: If CNPJ formatter options have
                an invalid type.
            ``CnpjFormatterOptionsHiddenRangeInvalidException``: If CNPJ
                formatter ``hidden_start`` or ``hidden_end`` are out of valid
                range.
            ``CnpjFormatterOptionsForbiddenKeyCharacterException``: If a CNPJ
                formatter key option contains a disallowed character.
            ``CnpjGeneratorOptionsTypeError``: If CNPJ generator options have
                an invalid type.
            ``CnpjGeneratorOptionPrefixInvalidException``: If CNPJ generator
                ``prefix`` is invalid.
            ``CnpjGeneratorOptionTypeInvalidException``: If CNPJ generator
                ``type`` is not allowed.
            ``CnpjValidatorOptionsTypeError``: If CNPJ validator options have
                an invalid type.
            ``CnpjValidatorOptionTypeInvalidException``: If CNPJ validator
                ``type`` is not allowed.
            ``CpfFormatterOptionsTypeError``: If CPF formatter options have an
                invalid type.
            ``CpfFormatterOptionsHiddenRangeInvalidException``: If CPF
                formatter ``hidden_start`` or ``hidden_end`` are out of valid
                range.
            ``CpfFormatterOptionsForbiddenKeyCharacterException``: If a CPF
                formatter key option contains a disallowed character.
            ``CpfGeneratorOptionsTypeError``: If CPF generator options have an
                invalid type.
            ``CpfGeneratorOptionPrefixInvalidException``: If CPF generator
                ``prefix`` is invalid.
        """
        if cpf is not None:
            self._cpf = _resolve_utils(CpfUtils, cpf)
        elif cpf_formatter is not None or cpf_generator is not None:
            self._cpf = CpfUtils(formatter=cpf_formatter, generator=cpf_generator)
        else:
            self._cpf = CpfUtils()

        if cnpj is not None:
            self._cnpj = _resolve_utils(CnpjUtils, cnpj)
        elif (
            cnpj_formatter is not None
            or cnpj_generator is not None
            or cnpj_validator is not None
        ):
            self._cnpj = CnpjUtils(
                formatter=cnpj_formatter,
                generator=cnpj_generator,
                validator=cnpj_validator,
            )
        else:
            self._cnpj = CnpjUtils()

    @property
    def cnpj(self) -> CnpjUtils:
        """Access the CNPJ utilities instance."""
        return self._cnpj

    @cnpj.setter
    def cnpj(self, value: CnpjUtils | Mapping[str, Any] | None) -> None:
        """Set the active CNPJ utilities instance.

        It is flexible and can handle any of these inputs:

        1. A complete new instance of :class:`CnpjUtils`
        2. A mapping of :class:`CnpjUtils` component settings
        3. A partial mapping with options for the CNPJ utilities
        4. ``None`` to create a brand new instance of :class:`CnpjUtils`
           with the default options

        Note that this resets the CNPJ utilities instance completely. Any
        previous options will be overridden. To alter only a single option or
        a few options of the existing instance, access it directly and use the
        CNPJ utilities' setters and methods (for example,
        ``utils.cnpj.generator.options.type = 'numeric'``).

        Raises:
            ``CnpjFormatterOptionsTypeError``: If formatter options have an
                invalid type.
            ``CnpjFormatterOptionsHiddenRangeInvalidException``: If formatter
                ``hidden_start`` or ``hidden_end`` are out of valid range.
            ``CnpjFormatterOptionsForbiddenKeyCharacterException``: If a
                formatter key option contains a disallowed character.
            ``CnpjGeneratorOptionsTypeError``: If generator options have an
                invalid type.
            ``CnpjGeneratorOptionPrefixInvalidException``: If generator
                ``prefix`` is invalid.
            ``CnpjGeneratorOptionTypeInvalidException``: If generator ``type``
                is not allowed.
            ``CnpjValidatorOptionsTypeError``: If validator options have an
                invalid type.
            ``CnpjValidatorOptionTypeInvalidException``: If validator
                ``type`` is not allowed.
        """
        self._cnpj = _resolve_utils(CnpjUtils, value)

    @property
    def cpf(self) -> CpfUtils:
        """Access the CPF utilities instance."""
        return self._cpf

    @cpf.setter
    def cpf(self, value: CpfUtils | Mapping[str, Any] | None) -> None:
        """Set the active CPF utilities instance.

        It is flexible and can handle any of these inputs:

        1. A complete new instance of :class:`CpfUtils`
        2. A mapping of :class:`CpfUtils` component settings
        3. A partial mapping with options for the CPF utilities
        4. ``None`` to create a brand new instance of :class:`CpfUtils` with
           the default options

        Note that this resets the CPF utilities instance completely. Any
        previous options will be overridden. To alter only a single option or
        a few options of the existing instance, access it directly and use the
        CPF utilities' setters and methods (for example,
        ``utils.cpf.formatter.options.hidden = True``).

        Raises:
            ``CpfFormatterOptionsTypeError``: If formatter options have an
                invalid type.
            ``CpfFormatterOptionsHiddenRangeInvalidException``: If formatter
                ``hidden_start`` or ``hidden_end`` are out of valid range.
            ``CpfFormatterOptionsForbiddenKeyCharacterException``: If a
                formatter key option contains a disallowed character.
            ``CpfGeneratorOptionsTypeError``: If generator options have an
                invalid type.
            ``CpfGeneratorOptionPrefixInvalidException``: If generator
                ``prefix`` is invalid.
        """
        self._cpf = _resolve_utils(CpfUtils, value)


__all__ = ["BrUtils"]
