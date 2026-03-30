"""Nó do agente especialista em licitações (Lei 14.133/21)."""

from typing import Any, Dict, List

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from domain.entities.auditoria import AchadoAuditoria
from use_cases.agents.prompts import PROMPT_AGENTE_LICITACAO
from use_cases.state import AuditoriaState
from use_cases.state_normalization import edital_do_state


class ExtracaoLicitacao(BaseModel):
    """Schema Wrapper para forçar o LLM a extrair uma lista estruturada de achados."""

    achados_encontrados: list[AchadoAuditoria] = Field(
        default_factory=list,
        description="Lista completa de todos os achados de auditoria identificados neste documento.",
    )


class AgenteLicitacaoNode:
    """Nó Trabalhador especialista em Lei de Licitações."""

    def __init__(self, llm: BaseChatModel, tools: List[BaseTool]) -> None:
        # A ferramenta agora é injetada, o Use Case não sabe qual é a implementação real
        llm_with_tools = llm.bind_tools(tools)
        self.llm_chain = llm_with_tools.with_structured_output(ExtracaoLicitacao)

    def __call__(self, state: AuditoriaState) -> Dict[str, Any]:
        edital = edital_do_state(state.get("edital"))

        if not edital:
            return {"erros": ["Agente de Licitação falhou: Nenhum edital encontrado no Estado."]}

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

        try:
            print(f"[DEBUG] Invocando LLM para o processo {edital.numero_processo}...")
            resultado: ExtracaoLicitacao = self.llm_chain.invoke(messages)
            print(f"[DEBUG] Resposta do LLM recebida com {len(resultado.achados_encontrados)} achados.")
            return {
                "achados": resultado.achados_encontrados,
                "analises_concluidas": ["licitacao"],
            }

        except Exception as e:
            return {"erros": [f"Erro na execução do Agente de Licitação: {str(e)}"]}
