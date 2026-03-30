import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from adapters.tools.busca_leis import buscar_lei_14133
from use_cases.workflows.grafo import construir_grafo_auditoria

# Carrega as variáveis de ambiente para o Studio
load_dotenv()

# Prevenção de falha caso o Studio tente fazer parse do arquivo sem a chave exportada
api_key = os.getenv("OPENAI_API_KEY", "chave_nao_configurada_no_env")

# Instancia o LLM padrão para a visualização local
llm_studio = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

# A variável 'graph' é o ponto de entrada que o LangGraph Studio irá procurar
graph = construir_grafo_auditoria(
    llm=llm_studio, 
    ferramentas_licitacao=[buscar_lei_14133]
)
