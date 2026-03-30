"""Conversão de valores do State (dict após serialização) para entidades Pydantic do domínio."""

from __future__ import annotations

from typing import Any

from domain.entities.auditoria import AchadoAuditoria, ParecerTecnico
from domain.entities.documentos import Edital


def edital_do_state(valor: Edital | dict[str, Any] | None) -> Edital | None:
    """Garante `Edital` mesmo quando o LangGraph entrega `dict` no checkpoint."""
    if valor is None:
        return None
    if isinstance(valor, Edital):
        return valor
    if isinstance(valor, dict):
        return Edital.model_validate(valor)
    msg = f"Tipo inválido para edital no State: {type(valor)!r}"
    raise TypeError(msg)


def achado_do_state(valor: AchadoAuditoria | dict[str, Any]) -> AchadoAuditoria:
    if isinstance(valor, AchadoAuditoria):
        return valor
    if isinstance(valor, dict):
        return AchadoAuditoria.model_validate(valor)
    msg = f"Tipo inválido para achado no State: {type(valor)!r}"
    raise TypeError(msg)


def achados_do_state(itens: list[Any]) -> list[AchadoAuditoria]:
    return [achado_do_state(a) for a in itens]


def parecer_do_state(valor: ParecerTecnico | dict[str, Any] | None) -> ParecerTecnico | None:
    if valor is None:
        return None
    if isinstance(valor, ParecerTecnico):
        return valor
    if isinstance(valor, dict):
        return ParecerTecnico.model_validate(valor)
    msg = f"Tipo inválido para parecer_final no State: {type(valor)!r}"
    raise TypeError(msg)
