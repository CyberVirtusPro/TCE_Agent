"""Ferramentas RAG para fundamentação normativa (camada de adapters)."""

from langchain_core.tools import tool


@tool
def buscar_lei_14133(query: str) -> str:
    """
    USE ESTA FERRAMENTA para buscar artigos, parágrafos e incisos exatos da Nova Lei de Licitações (Lei 14.133/21).
    Forneça termos de busca claros e objetivos (ex: 'dispensa de licitação para obras limite de valor').
    Retorna o texto da lei e da jurisprudência do TCERJ em formato string.
    """
    # TODO: Implementar conexão real com Pinecone/ChromaDB.
    # Por enquanto, retorna um mock seguro para não quebrar o State.
    return f"Resultados simulados da base de conhecimento da Lei 14.133 para a query: {query}"
