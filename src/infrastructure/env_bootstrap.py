"""Carrega `.env` e alinha variáveis LangSmith/LangChain antes de importar LangChain."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[2]


def configurar_ambiente_antes_do_langchain() -> None:
    """Deve ser chamado antes de `import langchain*` / `langgraph*` para o tracing funcionar."""
    load_dotenv(_REPO_ROOT / ".env")
    _sincronizar_langsmith_para_langchain()


def _sincronizar_langsmith_para_langchain() -> None:
    """LangChain ainda usa em muitos caminhos `LANGCHAIN_*`; o .env pode usar só `LANGSMITH_*`."""
    smith_on = os.getenv("LANGSMITH_TRACING", "").lower() in ("true", "1", "yes")
    chain_on = os.getenv("LANGCHAIN_TRACING_V2", "").lower() in ("true", "1", "yes")
    if smith_on and not chain_on:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"

    api = (os.getenv("LANGSMITH_API_KEY") or "").strip()
    if api and not (os.getenv("LANGCHAIN_API_KEY") or "").strip():
        os.environ["LANGCHAIN_API_KEY"] = api

    project = (os.getenv("LANGSMITH_PROJECT") or "").strip()
    if project and not (os.getenv("LANGCHAIN_PROJECT") or "").strip():
        os.environ["LANGCHAIN_PROJECT"] = project
