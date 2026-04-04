#!/bin/bash
# Interrompe o script caso ocorra algum erro (exceto nos loops que controlamos)
set -e

# Se DJANGO_ENV não estiver definida, assume 'development' como padrão
ENV_TYPE=${DJANGO_ENV:-development}

# ESPERA PELO BANCO DE DADOS
if [ "$ENV_TYPE" != "development" ]; then
    echo "Aguardando o banco de dados MySQL inicializar completamente..."
    # Tenta conectar usando python (-c para comando) e sai quando conseguir
    # max 30 tentativas, esperando 1 seg entre elas
    MAX_TRIES=30
    TRIES=0
    while ! python -c "
import sys, os, django
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    sys.exit(0)
except Exception:
    sys.exit(1)
" > /dev/null 2>&1; do
        TRIES=$((TRIES+1))
        if [ "$TRIES" -ge "$MAX_TRIES" ]; then
            echo >&2 "Erro: Banco de dados não está disponível após $MAX_TRIES tentativas. Cancelando."
            exit 1
        fi
        echo "Banco de dados ainda não pronto. Tentando novamente em 2 segundos... ($TRIES/$MAX_TRIES)"
        sleep 2
    done
    echo "Conexão com o banco de dados estabelecida com sucesso!"
fi

echo "Executando migrações do banco de dados..."
python manage.py migrate

if [ "$ENV_TYPE" = "development" ]; then
    echo "Ambiente de Desenvolvimento detectado."
    echo "Iniciando servidor de desenvolvimento (runserver) com SQLite..."
    exec python manage.py runserver 0.0.0.0:80
else
    echo "Ambiente $ENV_TYPE detectado."
    echo "Coletando arquivos estáticos para o WhiteNoise..."
    python manage.py collectstatic --noinput
    
    echo "Iniciando Gunicorn..."
    exec gunicorn core.wsgi:application --bind 0.0.0.0:80
fi
