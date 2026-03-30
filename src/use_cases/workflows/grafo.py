"""Factory do grafo de auditoria (LangGraph)."""

from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from use_cases.agents.licitacao import AgenteLicitacaoNode
from use_cases.agents.relator import AgenteRelatorNode
from use_cases.agents.supervisor import SupervisorNode
from use_cases.state import AuditoriaState


def construir_grafo_auditoria(llm: BaseChatModel) -> CompiledStateGraph:
    """
    Constrói e compila o grafo de auditoria do TCERJ.
    Recebe as dependências externas (LLM) via Injeção de Dependência.
    """
    builder = StateGraph(AuditoriaState)

    # 1. Adicionando os Nós (Instanciando com a injeção do LLM)
    builder.add_node("supervisor", SupervisorNode(llm))
    builder.add_node("agente_licitacao", AgenteLicitacaoNode(llm))
    builder.add_node("agente_relator", AgenteRelatorNode(llm))

    # 2. Definindo o Fluxo Principal
    # A esteira sempre começa pelo Maestro (Supervisor)
    builder.add_edge(START, "supervisor")

    # O Supervisor retorna Command(goto=...), então não precisamos de add_conditional_edges aqui.
    # Quando um especialista termina seu trabalho, ele DEVE devolver para o Supervisor avaliar o que fazer a seguir.
    builder.add_edge("agente_licitacao", "supervisor")

    # O Relator é o fim da linha. Após ele, encerramos a esteira.
    builder.add_edge("agente_relator", END)

    # Compila o grafo aplicando o limite de segurança exigido pela nossa Rule
    return builder.compile()
