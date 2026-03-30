"""Ferramentas RAG para fundamentação normativa (camada de adapters)."""

import os

from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient


@tool
def buscar_lei_14133(query: str) -> str:
    """
    USE ESTA FERRAMENTA para buscar artigos, parágrafos e incisos exatos da Nova Lei de Licitações (Lei 14.133/21).
    Forneça termos de busca claros e objetivos (ex: 'dispensa de licitação para obras limite de valor').
    Retorna o texto da lei e da jurisprudência do TCERJ em formato string.
    """
    try:
        print(f"\n[DEBUG] BUSCANDO NO QDRANT: {query}")

        # Pega as configurações do ambiente (ou usa os padrões locais do Docker)
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "documentos_legais")

        # Instancia o cliente do Qdrant e o modelo de embeddings (o mesmo usado na ingestão)
        client = QdrantClient(url=qdrant_url)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # 1. Converte a pergunta do agente em um vetor matemático
        query_vector = embeddings.embed_query(query)

        # 2. Faz a busca semântica no Qdrant (trazendo os 4 trechos mais relevantes)
        resultados = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=4,
        )

        if not resultados:
            return "Nenhum artigo correspondente encontrado na base de documentos legais para esta busca."

        # 3. Formata os resultados recuperados para o LLM ler
        textos_encontrados = []
        for res in resultados:
            payload = res.payload if isinstance(res.payload, dict) else {}
            # O LangChain geralmente salva no 'page_content', mas garantimos um fallback para 'texto'
            texto = payload.get("page_content", "") or payload.get("texto", str(payload))
            textos_encontrados.append(f"- {texto}")

        return "\n\n".join(textos_encontrados)

    except Exception as e:
        # Retornamos o erro como string para o LLM saber que a ferramenta falhou, evitando o crash da esteira
        return (
            f"Falha de infraestrutura ao acessar o banco de leis (Qdrant): {str(e)}. "
            "Prossiga com seu conhecimento prévio, se possível, mas avise o usuário."
        )
