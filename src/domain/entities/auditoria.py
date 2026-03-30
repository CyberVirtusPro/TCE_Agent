"""Entidades de achados de auditoria e parecer técnico (domínio TCERJ)."""

from pydantic import BaseModel, Field


class AchadoAuditoria(BaseModel):
    """Achado identificado durante a análise de conformidade."""

    descricao: str = Field(description="Descrição objetiva do achado")
    artigo_lei: str = Field(
        default="",
        description="Referência normativa associada ao achado (artigo, inciso ou lei)",
    )
    quote: str = Field(
        default="",
        description="Trecho exato do documento que fundamenta o achado",
    )
    justificativa: str = Field(
        default="",
        description="Fundamentação técnica do achado à luz da norma",
    )
    status_conformidade: str = Field(
        default="",
        description="Avaliação de conformidade (ex.: conforme, não conforme, risco)",
    )
    recomendacao: str = Field(
        default="",
        description="Recomendação ao órgão, quando couber",
    )


class ParecerTecnico(BaseModel):
    """Parecer técnico consolidado emitido após a análise."""

    resumo_executivo: str = Field(
        description="Síntese oficial da situação auditada",
    )
    achados: list[AchadoAuditoria] = Field(
        default_factory=list,
        description="Lista exata dos achados produzidos pelos especialistas",
    )
    conclusao_aprovacao: bool = Field(
        description="True se aprovado; False se reprovado (ex.: achado NAO_CONFORME)",
    )
