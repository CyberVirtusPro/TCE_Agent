---
name: criar-avaliador-langsmith
description: Use esta skill para gerar um script de avaliação (LLM-as-a-judge) que testa um agente ou Grafo do LangGraph contra um dataset previamente criado no LangSmith.
---
# Workflow: Criar Avaliador (Evaluator) no LangSmith

Siga os passos rigorosamente para implementar uma rotina de avaliação de agentes usando a biblioteca `openevals` e o SDK do LangSmith:

1. **Importações Necessárias:** Importe a função `evaluate` da biblioteca `langsmith` e os prompts avaliadores embutidos da `openevals` (como `CORRECTNESS_PROMPT`).
2. **Definir a Função Alvo (Target Function):** Isole a função que executa o agente. A função deve aceitar um dicionário de `inputs`, invocar o grafo compilado (`compiled_graph.invoke`) e garantir que o `run_id` seja capturado e associado à execução.
3. **Configurar o LLM Avaliador (LLM-as-a-judge):** Configure uma função que receba `inputs`, `outputs` e `reference_outputs`. Utilize um LLM de alta capacidade (ex: GPT-4o ou Claude 3.5 Sonnet) para julgar métricas jurídicas críticas, verificando rigorosamente a Fidelidade (Faithfulness) à lei e a exatidão das citações obrigatórias exigidas pelo TCERJ.
4. **Executar a Avaliação:** Chame o método `evaluate()` passando a função alvo, o nome do dataset, a lista de avaliadores configurados e um prefixo de experimento claro para o projeto (exemplo: `experiment_prefix="tcerj-auditoria-v1"`).
5. **Console Output:** Imprima no console o link gerado pela avaliação para facilitar o acesso direto à interface visual do LangSmith pelos engenheiros.