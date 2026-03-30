# Especificação do Projeto: Sistema Multi-Agente Jurídico

## Visão Geral
Sistema de IA baseado em LangGraph para confrontar contratos com bases legais (Licitações (14133), Lei da transparência, Tributário), quebrando documentos e analisando partes em paralelo.

## Stack Tecnológica
- Python 3.12+
- LangGraph (Orquestração de Agentes e Grafos de Estado)
- LangChain (Integração de LLMs e Tools)
- Bancos de Dados Vetoriais (Pinecone/Chroma)
- Pydantic (Validação rigorosa de schemas e saídas estruturadas)
- **LangSmith (Observabilidade, Tracing de requisições e Avaliação/Evaluations)**

## Fluxo Principal (LangGraph)
1. Recebimento do documento e quebra em partes.
2. Roteamento pelo Agente Supervisor para Especialistas.
3. Extração paralela (Parallel Fan-Out).
4. Verificação de Alucinação (Reflexive Loop).
5. Consolidação e formatação de saída.

## Requisitos de Telemetria e Qualidade
- **Observabilidade:** Todas as invocações de LLM e fluxos do LangGraph devem ser rastreados (traced) obrigatoriamente utilizando o LangSmith para permitir a auditoria das decisões da IA.
- **Avaliação Jurídica:** O sistema deve suportar baterias de testes *offline* (LLM-as-a-judge) para garantir a acurácia jurídica das respostas em relação aos datasets de referência (gabaritos).

## Checklist curto de conformidade (regras + AGENTS.md)

Usar antes de PR ou release; marcar ao concluir.

- [ ] **Documentação:** `instructions.md` e `roadmap.md` refletem o código (stack, fluxo, vetorial, limites).
- [ ] **API:** `src/infrastructure/server.py` expõe `app` FastAPI ou o `AGENTS.md` deixa de citar `uvicorn` até existir.
- [ ] **Domínio:** nenhum import de LangChain/LangGraph/prompts em `src/domain/`.
- [ ] **Use cases:** prompts só em `src/use_cases/agents/prompts.py`; ferramentas injetadas no nó de licitação (sem import direto do adapter no use case).
- [ ] **Estado:** `AuditoriaState` com reducers onde necessário; `analises_concluidas` evita loop supervisor ↔ licitação.
- [ ] **Tools:** saída serializável (`str`/`dict`/`list`); Qdrant com `try/except` retornando mensagem ao LLM em falha.
- [ ] **Segurança:** segredos só via `.env`; avaliar PII antes de enviar texto integral ao LLM quando o caso não exigir identificação.
- [ ] **LangGraph:** `recursion_limit` definido e documentado (recomendação das rules: 10–15 para auditoria simples).
- [ ] **LangSmith:** `.env` carregado antes dos imports do LangChain (`env_bootstrap`); projeto correto no painel.
- [ ] **Testes:** `pytest tests/domain/` verde; mocks de infra nos testes de use cases quando existirem.
- [ ] **Evals:** script ou pipeline LangSmith (LLM-as-judge) para o grafo ou nó crítico, quando houver dataset.
