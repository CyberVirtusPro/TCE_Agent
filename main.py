"""Ponto de entrada: composition root e simulação da esteira de auditoria."""

from __future__ import annotations

import asyncio
import os
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

# Permite executar `python main.py` na raiz sem configurar PYTHONPATH manualmente
_SRC = Path(__file__).resolve().parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

# Dependência de Infraestrutura (Driver de LLM)
from langchain_openai import ChatOpenAI

# Adapters (composition root: instâncias concretas de ferramentas)
from adapters.tools.busca_leis import buscar_lei_14133

# Importações do nosso Domínio e Casos de Uso
from domain.entities.documentos import Edital
from use_cases.workflows.grafo import construir_grafo_auditoria

# Carrega as variáveis do arquivo .env
load_dotenv()


async def executar_auditoria_simulada() -> None:
    print("Iniciando o Sistema Multi-Agente do TCERJ...\n")

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "Defina OPENAI_API_KEY no arquivo .env na raiz do projeto antes de executar a simulação."
        )

    # 1. COMPOSITION ROOT: Instanciamos a infraestrutura externa (LLM)
    # Lembre-se de ter a variável OPENAI_API_KEY no seu .env
    # Dica: Use model="gpt-4o-mini" para testes rápidos e baratos
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Injetamos o LLM na nossa fábrica de grafos
    print("[Sistema] Compilando o Grafo de Auditoria...")
    grafo_compilado = construir_grafo_auditoria(llm, ferramentas_licitacao=[buscar_lei_14133])

    # 2. CRIANDO O MOCK DO DOCUMENTO (A "Esteira")
    edital_teste = Edital(
        id_documento="EDITAL-2026-001",
        data_ingestao=date.today(),
        numero_processo="SEI-12345/2026",
        orgao_jurisdicionado="Prefeitura de Nova Iguaçu",
        objeto_licitacao="Contratação de empresa para reforma de escolas municipais.",
        modalidade="Dispensa de Licitação",
        valor_estimado=250000.00,
        texto_integral=(
            "O prefeito de Nova Iguaçu resolve contratar por dispensa de licitação "
            "a empresa X para reforma das escolas, com base na urgência das chuvas. "
            "O valor total será de R$ 250.000,00 pagos à vista."
        ),
    )

    # 3. PREPARANDO A MOCHILA (STATE)
    estado_inicial = {
        "edital": edital_teste,
        "achados": [],
        "parecer_final": None,
        "erros": [],
        "metadata": {
            "run_id": "simulacao-001",
            "law_version": "14133/21",
            "orgao_emissor": "TCERJ",
        },
    }

    print(f"\n[Sistema] Iniciando auditoria do Processo: {edital_teste.numero_processo}")
    print(f"[Sistema] Objeto: {edital_teste.objeto_licitacao}\n")

    # 4. EXECUTANDO O GRAFO
    # O limite de recursão (recursion_limit) nos protege contra loops infinitos de alucinação
    config = {"recursion_limit": 15}

    # Executamos o grafo de forma assíncrona (ideal para o FastAPI futuramente)
    resultado_final = await grafo_compilado.ainvoke(estado_inicial, config=config)

    # 5. EXIBINDO OS RESULTADOS (PARECER TÉCNICO)
    parecer = resultado_final.get("parecer_final")
    erros = resultado_final.get("erros", [])

    if erros:
        print("--- ERROS ENCONTRADOS NO FLUXO ---")
        for erro in erros:
            print(f"- {erro}")

    if parecer:
        print("====== PARECER TÉCNICO CONSOLIDADO ======")
        print(f"Status Final: {'APROVADO' if parecer.conclusao_aprovacao else 'REPROVADO/DEVOLVIDO'}")
        print(f"Resumo Executivo:\n{parecer.resumo_executivo}\n")
        print("--- ACHADOS DE AUDITORIA ---")
        for idx, achado in enumerate(parecer.achados, 1):
            print(f"{idx}. [{achado.status_conformidade}] Lei: {achado.artigo_lei}")
            print(f"   Justificativa: {achado.justificativa}")
            print(f"   Evidência (Quote): \"{achado.quote}\"")
            if achado.recomendacao:
                print(f"   Recomendação: {achado.recomendacao}")
            print("-" * 40)
    else:
        print("\n[Atenção] Nenhum parecer final foi gerado pelo Relator.")


if __name__ == "__main__":
    # Roda o fluxo de forma assíncrona
    asyncio.run(executar_auditoria_simulada())
