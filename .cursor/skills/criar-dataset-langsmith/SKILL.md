---
name: criar-dataset-langsmith
description: Use esta skill para automatizar a criação de um dataset de referência (gabarito jurídico) no LangSmith, contendo inputs (trechos e leis) e outputs esperados (reference_outputs).
---
# Workflow: Criar Dataset no LangSmith

Siga os seguintes passos para registrar um novo dataset de avaliação no LangSmith de forma idempotente e segura:

1. **Instanciar o Cliente:** Importe e instancie o cliente de telemetria utilizando o comando `from langsmith import Client`.
2. **Definir o Dataset:** Crie a estrutura primária utilizando o método `client.create_dataset`, fornecendo um nome claro e uma descrição focada no propósito da auditoria corporativa em questão.
3. **Estruturar os Pares de Entrada e Saída:** Modele uma lista de exemplos. Os `inputs` devem conter o trecho original do documento e a legislação pertinente. Os `outputs` devem espelhar perfeitamente o schema Pydantic oficial, incluindo obrigatoriamente os campos de validação, a justificativa técnica e o "quote" exato da evidência.
4. **Fazer o Upload dos Exemplos:** Itere de forma segura sobre a lista estruturada de dicionários e registre cada caso individualmente utilizando o comando `client.create_example()`.
5. **Tratamento de Erros:** Implemente verificações defensivas utilizando `client.has_dataset` antes da criação, evitando duplicidades, falhas na sobreposição de dados ou quebras silenciosas no script.