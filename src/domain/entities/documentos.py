"""Entidades de documentos submetidos à auditoria (domínio TCERJ)."""

from datetime import date

from pydantic import BaseModel, Field


class Edital(BaseModel):
    """Edital ou instrumento convocatório objeto de análise."""

    identificacao: str = Field(
        default="",
        description="Identificação do edital (número, processo ou título)",
    )
    data_ingestao: date | None = Field(
        default=None,
        description="Data de ingestão do documento no sistema",
    )
    orgao_jurisdicionado: str = Field(
        default="",
        description="Órgão jurisdicionado responsável pelo ato",
    )
    valor_estimado: float = Field(
        default=0.0,
        description="Valor estimado da contratação, quando aplicável",
    )
    id_documento: str = Field(
        default="",
        description="Identificador interno do documento para rastreabilidade",
    )
    objeto_licitacao: str = Field(
        default="",
        description="Objeto da licitação conforme o instrumento convocatório",
    )
    modalidade: str = Field(
        default="",
        description="Modalidade de licitação (ex.: pregão, concorrência, leilão)",
    )
    numero_processo: str = Field(
        default="",
        description="Número do processo ou procedimento licitatório",
    )
    texto_integral: str = Field(
        default="",
        description="Texto integral do instrumento convocatório para auditoria",
    )
