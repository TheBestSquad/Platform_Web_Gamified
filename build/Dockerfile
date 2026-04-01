# Usa a imagem oficial do Python, versão slim para ser mais leve
FROM python:3.12-slim

# Impede o Python de gravar arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que a saída do Python seja enviada direto para o terminal (útil para logs)
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e as instala
COPY build/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto para o diretório de trabalho
COPY . /app/

# Expõe a porta que o servidor de desenvolvimento do Django utilizará
EXPOSE 80
