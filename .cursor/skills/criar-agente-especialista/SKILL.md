---
name: criar-agente-especialista
description: Use esta skill quando o usuário pedir para criar um novo agente trabalhador especialista (ex: Agente Tributário, Agente LGPD) para o sistema LangGraph.
---
# Workflow: Criação de Agente Especialista

Siga estes passos rigorosamente para adicionar um novo agente ao ecossistema, respeitando a Clean Architecture e os padrões do TCERJ:

1. **Definição de Contrato (Entities):** Crie os schemas Pydantic de entrada e saída na camada de Domínio. Garanta obrigatoriamente que o schema de saída contenha as propriedades exigidas pelo Tribunal: `justificativa`, `status_conformidade`, `quote` (trecho exato da evidência extraída) e `artigo_lei`.
2. **Criação das Tools (Adapters):** Crie as ferramentas decoradas com `@tool` específicas para buscar no banco vetorial as leis do escopo deste agente. Escreva uma docstring detalhada e imperativa, explicando ao LLM as regras exatas de quando acionar ou ignorar a ferramenta.
3. **Criação do Nó do Agente (Use Cases):** Crie a função do nó recebendo o `TypedDict` State global do LangGraph. Configure o LLM atrelando as ferramentas (com `bind_tools`) e force a saída estruturada legal usando a função `.with_structured_output()`. O System Prompt deve impor o tom de voz oficial e impessoal.
4. **Registro no Supervisor e no Grafo:** Adicione a especialidade no roteamento do Agente Supervisor preferencialmente utilizando o padrão `Command(goto='nome_do_agente')`. Registre o nó no grafo principal via `graph.add_node` e mapeie as arestas de retorno.