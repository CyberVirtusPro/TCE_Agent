---
name: criar-ferramenta-rag
description: Use esta skill para implementar uma nova ferramenta de busca semântica (RAG) em bases legais para ser consumida pelos agentes.
---
# Workflow: Criação de Ferramenta RAG

Siga os passos abaixo para construir adaptadores de busca vetorial eficientes, seguros e alinhados à LGPD:

1. **Infraestrutura (Frameworks & Drivers):** Localize o módulo de conexão com o banco vetorial. Implemente o método de `similarity_search` isolando completamente as credenciais e lógicas de banco (conexões TCP/HTTP) da regra de negócio central.
2. **Criação da Interface (Adapters):** Implemente a função de busca decorada com `@tool`. Utilize Type Hints estritos para os argumentos de entrada. Redija uma docstring abrangente que oriente o agente a distinguir corretamente entre a busca na Legislação Federal e nos Normativos internos do TCERJ.
3. **Privacidade e Sanitização (LGPD):** Antes de enviar a query de busca final para o banco de dados vetorial ou para o LLM de embeddings, garanta a implementação de um filtro ou máscara para anonimizar dados sensíveis (PII) extraídos acidentalmente do input do usuário.
4. **Integração de Resiliência:** Utilize blocos `try/except` para capturar falhas de infraestrutura. Em caso de erro de conexão com o banco vetorial, retorne uma string semântica orientando o LLM sobre o problema de rede, permitindo que o modelo decida abortar ou tentar uma estratégia alternativa de raciocínio.