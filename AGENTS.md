# Instruções Globais para Agentes de IA (AGENTS.md)

Este arquivo serve como o "System Prompt Global" para agentes de IA (como Cursor IDE) que operam neste repositório. Ele define o contexto do projeto, a stack tecnológica e as regras inegociáveis.

## 🏛️ Contexto do Projeto (Domínio)
- **Organização:** Tribunal de Contas do Estado do Rio de Janeiro (TCERJ).
- **Objetivo:** Sistema Multi-Agente de nível de produção para auditoria inteligente, extração estruturada e emissão de pareceres de conformidade em documentos e contratos corporativos.
- **Domínio Legal:** O sistema confronta documentos com bases legais rigorosas (ex: Lei de Licitações 14.133/21, LGPD, Normativos Internos e Jurisprudência do TCERJ).
- **Tom de Voz da IA:** Todo output gerado pelo sistema para o usuário final deve ser técnico, impessoal, fundamentado em leis e seguir o padrão oficial de redação de auditoria.

## 🛠️ Stack Tecnológica
- **Linguagem:** Python (Tipagem Estrita com Type Hints).
- **Orquestração de IA:** LangGraph (Stateful, Supervisor-Worker, Reflexive RAG).
- **Modelagem de Dados:** Pydantic (obrigatório para schemas e validação).
- **Observabilidade e QA:** LangSmith (Tracing e LLM-as-a-judge via `openevals`).
- **Web Framework:** FastAPI.

## 📐 Diretrizes de Arquitetura (Clean Architecture & SOLID)
- **Isolamento Total:** A lógica de negócios (Domínio/Entities) deve ser puramente baseada em Pydantic e Python nativo. É **estritamente proibido** importar LangChain, LangGraph, prompts ou dependências de banco de dados na camada de Domínio.
- **Gerenciamento de Estado (LangGraph):** Os estados dos agentes devem ser obrigatoriamente definidos usando `TypedDict` explícitos. Utilize reducers (ex: `Annotated[list, add]`) para evitar perda silenciosa de dados em execuções de nós paralelos (Fan-Out).
- **Atenção às Rules (.mdc):** Consulte sempre os arquivos na pasta `.cursor/rules/` para aplicar os padrões específicos de infraestrutura, segurança (LGPD) e testes.

## 🚀 Comandos de Build, Testes e Observabilidade
- **Testes Unitários/Domínio:** `pytest tests/domain/`
- **Executar CLI (Simulação do Grafo):** `python main.py`
- **Executar API Web (FastAPI):** `uvicorn src.infrastructure.server:app --reload`
- **Avaliação de IA (LangSmith):** O agente deve priorizar a criação e execução de scripts de avaliação (`LLM-as-a-judge`) para garantir *Correctness*, *Faithfulness* e *Relevance* nas saídas dos grafos.
- **Autocorreção:** O agente deve sempre tentar rodar comandos de testes programáticos após alterações e corrigir falhas de tipagem ou de assertions antes de finalizar uma tarefa.

## 🔄 Diretrizes de Pull Request e Entrega
- Antes de submeter ou finalizar um código, atualize os arquivos de documentação (como `instructions.md` e `roadmap.md`).
- Verifique rigorosamente se as saídas estruturadas dos LLMs (`.with_structured_output()`) estão mapeadas corretamente para os contratos Pydantic.
- Garanta que não há chaves de API "hardcoded" no código e que dados sensíveis de documentos (PII) possuem tratamento adequado.