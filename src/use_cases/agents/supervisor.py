from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from pydantic import BaseModel, Field

from use_cases.agents.prompts import PROMPT_SUPERVISOR
from use_cases.state import AuditoriaState
from use_cases.state_normalization import achados_do_state, edital_do_state


class RoteamentoSupervisor(BaseModel):
    """Schema Pydantic para forçar a saída estruturada do LLM no roteamento."""

    proximo_agente: Literal["agente_licitacao", "agente_relator"] = Field(
        ...,
        description="O nome exato do próximo nó a ser executado.",
    )
    justificativa: str = Field(
        ...,
        description="O motivo pelo qual este agente foi escolhido para atuar agora.",
    )


class SupervisorNode:
    """
    Nó do LangGraph responsável por atuar como Maestro/Router.
    Recebe o LLM via Injeção de Dependência.
    """

    def __init__(self, llm: BaseChatModel) -> None:
        # Forçamos o LLM a responder estritamente no formato do RoteamentoSupervisor
        self.llm_with_tool = llm.with_structured_output(RoteamentoSupervisor)

    def __call__(self, state: AuditoriaState) -> Command:
        edital = edital_do_state(state.get("edital"))
        achados = achados_do_state(list(state.get("achados", [])))

        if not edital:
            raise ValueError("O Estado não contém um Edital válido para análise.")

        # Montamos o contexto para o LLM entender o que já foi feito
        tipos_achados_realizados = [achado.artigo_lei for achado in achados]

        contexto_humano = (
            f"Documento a ser analisado: {edital.objeto_licitacao} (Modalidade: {edital.modalidade})\n"
            f"Quantidade de achados até o momento: {len(achados)}\n"
            f"Leis já apontadas nos achados: {tipos_achados_realizados}\n\n"
            f"Análises já finalizadas: {state.get('analises_concluidas', [])}\n\n"
            "Qual é o próximo agente especialista que deve atuar?"
        )

        messages = [
            SystemMessage(content=PROMPT_SUPERVISOR),
            HumanMessage(content=contexto_humano),
        ]

        # Invocamos o LLM que já está "preso" ao schema Pydantic
        decisao: RoteamentoSupervisor = self.llm_with_tool.invoke(messages)

        # O LangGraph 2026 usa Command para roteamento dinâmico
        return Command(
            goto=decisao.proximo_agente,
            update={
                # O supervisor não gera achados, então não altera o estado pesado.
                # Se quiséssemos logar o roteamento, poderíamos adicionar ao state aqui.
            },
        )
