import os
import sys
from pathlib import Path

# Garante imports de `src/` quando o Studio carrega este módulo pelo caminho do arquivo.
_SRC = Path(__file__).resolve().parent.parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from dotenv import load_dotenv

from infrastructure.env_bootstrap import configurar_ambiente_antes_do_langchain

configurar_ambiente_antes_do_langchain()

from langchain_openai import ChatOpenAI

from adapters.tools.busca_leis import buscar_lei_14133
from use_cases.workflows.grafo import construir_grafo_auditoria

# Idempotente
load_dotenv()

# Prevenção de falha caso o Studio tente fazer parse do arquivo sem a chave exportada
api_key = os.getenv("OPENAI_API_KEY", "chave_nao_configurada_no_env")

# Instancia o LLM padrão para a visualização local
llm_studio = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)

# A variável 'graph' é o ponto de entrada que o LangGraph Studio irá procurar
graph = construir_grafo_auditoria(
    llm=llm_studio,
    ferramentas_licitacao=[buscar_lei_14133],
)
