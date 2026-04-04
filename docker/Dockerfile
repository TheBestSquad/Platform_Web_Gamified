# Usa a imagem oficial do Python, versão slim para ser mais leve
FROM python:3.12-slim

# Impede o Python de gravar arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que a saída do Python seja enviada direto para o terminal (útil para logs)
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala as dependências (MySQL) do SO para garantir a infraestrutura imutável
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc pkg-config default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências e as instala
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto para o diretório de trabalho
COPY . /app/

# Dá permissão de execução ao script e corrige quebras de linha do Windows (CRLF -> LF)
RUN chmod +x /app/docker/entrypoint.sh && \
    sed -i 's/\r$//' /app/docker/entrypoint.sh

# Expõe a porta que o servidor de desenvolvimento do Django utilizará
EXPOSE 80

# Invoca o bash explicitamente para contornar problemas de permissão do volume local
ENTRYPOINT ["bash", "/app/docker/entrypoint.sh"]
