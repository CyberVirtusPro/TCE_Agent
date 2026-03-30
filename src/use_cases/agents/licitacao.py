"""Nó do agente especialista em licitações (Lei 14.133/21)."""

from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from adapters.tools.busca_leis import buscar_lei_14133
from domain.entities.auditoria import AchadoAuditoria
from use_cases.agents.prompts import PROMPT_AGENTE_LICITACAO
from use_cases.state import AuditoriaState


class ExtracaoLicitacao(BaseModel):
    """Schema Wrapper para forçar o LLM a extrair uma lista estruturada de achados."""

    achados_encontrados: list[AchadoAuditoria] = Field(
        default_factory=list,
        description="Lista completa de todos os achados de auditoria identificados neste documento.",
    )


class AgenteLicitacaoNode:
    """
    Nó Trabalhador especialista em Lei de Licitações.
    """

    def __init__(self, llm: BaseChatModel) -> None:
        # Amarramos a ferramenta ao LLM e forçamos a saída estruturada do nosso Domínio.
        llm_with_tools = llm.bind_tools([buscar_lei_14133])
        self.llm_chain = llm_with_tools.with_structured_output(ExtracaoLicitacao)

    def __call__(self, state: AuditoriaState) -> dict[str, Any]:
        edital = state.get("edital")

        if not edital:
            # Retorna para o reducer de erros sem quebrar o grafo
            return {"erros": ["Agente de Licitação falhou: Nenhum edital encontrado no Estado."]}

        # Prepara o contexto. Em um caso real, faríamos chunking se o texto fosse gigantesco.
        contexto_humano = (
            f"INFORMAÇÕES DO EDITAL:\n"
            f"Processo: {edital.numero_processo}\n"
            f"Objeto: {edital.objeto_licitacao}\n"
            f"Modalidade: {edital.modalidade}\n"
            f"Texto Integral: {edital.texto_integral}\n\n"
            "Realize a auditoria e extraia os achados."
        )

        messages = [
            SystemMessage(content=PROMPT_AGENTE_LICITACAO),
            HumanMessage(content=contexto_humano),
        ]

        # Invocação do modelo
        try:
            resultado: ExtracaoLicitacao = self.llm_chain.invoke(messages)

            # Retornamos APENAS a chave 'achados'. O reducer 'operator.add' no state.py
            # vai pegar essa lista e somar (append) com os achados que já existem na mochila.
            return {"achados": resultado.achados_encontrados}

        except Exception as e:
            return {"erros": [f"Erro na execução do Agente de Licitação: {str(e)}"]}
