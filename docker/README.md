# Execução da aplicação utilizando Docker

## Instalação do Docker

Instalamos o Docker utilizando o script oficial:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh \
  && sudo sh get-docker.sh \
  && rm get-docker.sh \
  && sudo usermod -aG docker $USER \
  && newgrp docker
```
## Execução da aplicação utilizando Docker e SQLite

Clone o repositório:
```bash
git clone https://github.com/TheBestSquad/Platform_Web_Gamified.git
```
Entre no diretório da aplicação:
```bash
cd Platform_Web_Gamified
```
Construa e execute a aplicação:
```bash
docker compose -f docker/docker-compose.yml up --build
```
Em outro terminal, entre no diretório da aplicação e crie um usuário administrador:
```bash
docker compose -f docker/docker-compose.yml exec web python manage.py createsuperuser
```
Acesse a aplicação em:
```bash
http://localhost/
```
E a interface de administração da aplicação em:
```bash
http://localhost/admin
```
Para encerrar a aplicação pressione CTRL+C no terminal da aplicação.

## Execução da aplicação utilizando Docker, MySQL e Gunicorn

Clone o repositório:
```bash
git clone https://github.com/TheBestSquad/Platform_Web_Gamified.git
```
Entre no diretório da aplicação:
```bash
cd Platform_Web_Gamified
```
Crie o arquivo .env com a seleção do ambiente e os parâmetros do banco de dados:
```bash
cat << 'EOF' > .env
# Seleção de ambiente: development, staging ou production
# staging e production utiliza MySQL
DJANGO_ENV=staging

# Variáveis do Django core/settings.py
SECRET_KEY=uma_chave_segura_gerada_aleatoriamente
# Liste o nameserver e o IP permitidos
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
# Força o modo de depuração ligado mesmo fora do ambiente development
DEBUG=True

# -------------------------------------------------------------
# Variáveis do Banco de Dados (ativadas em staging/production)
# -------------------------------------------------------------
COMPOSE_PROFILES=mysql
DB_HOST=db # Mude para o hostname ou endereço IP do banco de dados caso não use Docker
DB_NAME=gamification
DB_USER=gamification_user
DB_PASSWORD=senha_segura_da_aplicacao
DB_ROOT_PASSWORD=senha_super_segura_do_admin_db
DATABASE_URL=mysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:3306/${DB_NAME}
EOF
```
Construa utilizando o parâmetro do arquivo .env:
```bash
docker compose -f docker/docker-compose.yml --env-file .env --build
```
Execute a aplicação no terminal (ou com o parâmetro -d para utilizar o daemon):
```bash
docker compose -f docker/docker-compose.yml --env-file .env up
```
Entre no diretório da aplicação (execute outro terminal se necessário) e crie um usuário administrador com o comando:
```bash
docker compose -f docker/docker-compose.yml exec web python manage.py createsuperuser
```
Acesse a aplicação em:
```bash
http://localhost/
```
E a interface de administração da aplicação em:
```bash
http://localhost/admin
```
Para encerrar pressione CTRL+C no terminal da aplicação ou utilize:
```bash
docker compose -f docker/docker-compose.yml --env-file .env down
```
