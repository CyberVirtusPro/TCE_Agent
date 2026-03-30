"""Entidades de achados de auditoria e parecer técnico (domínio TCERJ)."""

from pydantic import BaseModel, Field


class AchadoAuditoria(BaseModel):
    """Achado identificado durante a análise de conformidade."""

    descricao: str = Field(description="Descrição objetiva do achado")


class ParecerTecnico(BaseModel):
    """Parecer técnico consolidado emitido após a análise."""

    texto: str = Field(description="Conteúdo integral do parecer")
