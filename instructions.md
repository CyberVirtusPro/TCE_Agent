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
