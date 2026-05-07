# Execução da aplicação utilizando Docker

## Instalação do WSL

Para utilizar o WSL é preciso que a virtualização esteja ativada. Para instalar precisamos executar o PowerShell do Windows como Administrador, na barra de pesquisa do menu iniciar digite “power” e clique em “Executar como Administrador” abaixo de “Windows PowerShell” no lado direito do menu.

No terminal do PowerShell executado como Administrador, cole o seguinte comando:
```bash
wsl --install
```
Depois da instalação dos recursos necessários é preciso reiniciar o computador.

Após o reinício uma janela de terminal do Linux vai abrir automaticamente (caso não abra automaticamente execute pelo atalho “Ubuntu” no menu iniciar) pedindo para definir um nome de usuário e senha.

Precisamos alterar a interface de rede do WSL para “mirrored” e ativar o “Loopback de endereço de Host”. No menu iniciar, digite “wsl” e abra o “WSL Settings”.

Selecione “Rede” no lado esquerdo da janela, mude o “Modo de rede” para “Mirrored” e ative o “Loopback de endereço de Host”.

Agora precisamos reiniciar o serviço do WSL, abra um prompt cmd (ou PowerShell) e digite:
```bash
wsl --shutdown
```
A partir daqui executamos os comandos no terminal do Ubuntu, inicie o terminal pelo menu iniciar digitando “Ubuntu”. Copie e cole os comandos dentro das caixas de textos no terminal utilizando SHIFT+INSERT para colar.

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
git clone https://github.com/leobrda/projetoIntegrador_I.git
```
Entre no diretório da aplicação:
```bash
cd projetoIntegrador_I
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
http://localhost:8000/
```
E a interface de administração da aplicação em:
```bash
http://localhost:8000/admin
```
Para encerrar a aplicação pressione CTRL+C no terminal da aplicação.

## Execução da aplicação utilizando Docker, MySQL e Gunicorn

Clone o repositório:
```bash
git clone https://github.com/leobrda/projetoIntegrador_I.git
```
Entre no diretório da aplicação:
```bash
cd projetoIntegrador_I
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
ALLOWED_HOSTS=localhost,127.0.0.1,*
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

Construa a imagem e execute a aplicação no terminal (ou com o parâmetro -d para utilizar o daemon):
```bash
docker compose -f docker/docker-compose.yml --env-file .env up --build
```
Entre no diretório da aplicação (execute outro terminal ou pressione 'D' para voltar ao terminal) e crie um usuário administrador com o comando:
```bash
docker compose -f docker/docker-compose.yml exec web python manage.py createsuperuser
```
Acesse a aplicação em:
```bash
http://localhost:8000/
```
E a interface de administração da aplicação em:
```bash
http://localhost:8000/admin
```
Para encerrar pressione CTRL+C no terminal da aplicação ou utilize:
```bash
docker compose -f docker/docker-compose.yml --env-file .env down
```
