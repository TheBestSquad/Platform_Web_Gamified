# Projeto Integrador I - UNIVESP (4º Semestre)
## Plataforma Gamificada web para o de ensino de informática

### 📝 Sobre o Projeto
Este projeto consiste no desenvolvimento de uma plataforma web gamificada focada no ensino de informática (14+ anos). A plataforma utiliza elementos de jogos (XP, conquistas e níveis) para tornar o aprendizado de ensino de informática mais envolvente e intuitivo.

### 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.12
* **Framework Web:** Django 6.x
* **Frontend:** HTML5, CSS3 (Tailwind CSS), JavaScript
* **Banco de Dados:** SQLite (Desenvolvimento)/MySQL (Produção)
* **Versionamento:** Git & GitHub

### 🚀 Estrutura de Versionamento
Adotamos um fluxo de trabalho baseado em branches para garantir a integridade do código:
* `main`: Versões estáveis e prontas para entrega.
* `develop`: Ambiente de integração de novas funcionalidades.
* `feature/*`: Desenvolvimento de requisitos específicos.

### 📦 Como Rodar o Projeto (Ambiente Local)
Instale as dependências do sistema operacional (no Linux/WSL):
```bash
sudo apt-get update && sudo apt-get install git python-is-python3 python3-dev python3-venv default-libmysqlclient-dev build-essential pkg-config
```
Clone o repositório:
```bash
git clone https://github.com/TheBestSquad/Platform_Web_Gamified.git
```
Entre no diretório da aplicação:
```bash
cd Platform_Web_Gamified
```
Crie um ambiente do python isolado:
```bash
python -m venv venv
```
Ative o ambiente virtual (no Linux/WSL)
```bash
source venv/bin/activate
```
Instale as dependências do python3
```bash
pip install -r requirements.txt
```
Inicialize o banco de dados com o comando:
```bash
python manage.py migrate
```
Crie uma conta para administração:
```bash
python manage.py createsuperuser
```
Execute a aplicação com o comando:
```bash
python manage.py runserver 0.0.0.0:8000
```
Acesse a aplicação em:
```bash
http://localhost:8000/
```
E a interface de administração da aplicação em:
```bash
http://localhost:8000/admin
```
Para encerrar pressione CTRL+C no terminal da aplicação e para desativar o ambiente virtual do python use o comando:
```bash
deactivate
```
