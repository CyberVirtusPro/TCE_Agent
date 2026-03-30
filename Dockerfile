# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instala dependências de sistema necessárias para o PyMuPDF e Qdrant Client
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de configuração de dependências
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copia o código fonte
COPY . .

# Expõe a porta padrão da API do LangGraph
EXPOSE 2024

# Comando para iniciar o servidor do LangGraph
CMD ["langgraph", "dev", "--host", "0.0.0.0", "--port", "2024"]