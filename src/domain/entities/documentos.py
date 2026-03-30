"""Entidades de documentos submetidos à auditoria (domínio TCERJ)."""

from pydantic import BaseModel, Field


class Edital(BaseModel):
    """Edital ou instrumento convocatório objeto de análise."""

    identificacao: str = Field(description="Identificação do edital (número, processo ou título)")
