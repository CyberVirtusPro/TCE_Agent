"""Factory do grafo de auditoria (LangGraph)."""

from typing import List

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from use_cases.agents.licitacao import AgenteLicitacaoNode
from use_cases.agents.relator import AgenteRelatorNode
from use_cases.agents.supervisor import SupervisorNode
from use_cases.state import AuditoriaState


def construir_grafo_auditoria(
    llm: BaseChatModel,
    ferramentas_licitacao: List[BaseTool],
) -> CompiledStateGraph:
    """
    Constrói e compila o grafo de auditoria do TCERJ.
    Recebe as dependências externas (LLM e ferramentas dos adapters) via Injeção de Dependência.
    """
    builder = StateGraph(AuditoriaState)

    builder.add_node("supervisor", SupervisorNode(llm))
    builder.add_node("agente_licitacao", AgenteLicitacaoNode(llm, tools=ferramentas_licitacao))
    builder.add_node("agente_relator", AgenteRelatorNode(llm))

    builder.add_edge(START, "supervisor")
    builder.add_edge("agente_licitacao", "supervisor")
    builder.add_edge("agente_relator", END)

    return builder.compile()
