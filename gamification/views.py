from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
# IMPORTAÇÃO PARA MODELOS CUSTOMIZADOS
from django.contrib.auth import get_user_model
User = get_user_model()

@login_required 
def home_view(request):
    return render(request, 'home.html')

def cadastro_view(request):
    # Se o formulário foi enviado (clicou no botão)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_nascimento = request.POST.get('data_nascimento')
        instituicao = request.POST.get('instituicao')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_confirmacao = request.POST.get('senha_confirmacao')
        senha_confirmacao = request.POST.get('senha_confirmacao')
        
        # Dicionário para devolver os dados digitados e evitar que o form limpe
        contexto = {
            'nome': nome,
            'data_nascimento': data_nascimento,
            'instituicao': instituicao,
            'email': email
        }

        # 1. Validação: as senhas precisam ser iguais
        if senha != senha_confirmacao:
            contexto['erro_campo'] = 'senha_confirmacao'
            contexto['erro_mensagem'] = 'As senhas não coincidem.'
            return render(request, 'cadastro.html', contexto)

        # 2. Validação: o email não pode já existir
        if User.objects.filter(username=email).exists():
            contexto['erro_campo'] = 'email'
            contexto['erro_mensagem'] = 'Este email já está cadastrado.'
            return render(request, 'cadastro.html', contexto)

        # 3. Criação do usuário customizado
        user = User.objects.create_user(username=email, email=email, password=senha)
        user.first_name = nome
        user.data_nascimento = data_nascimento
        user.instituicao = instituicao
        user.save()
        
        # 4. RBAC: associação ao grupo Alunos
        grupo_alunos, created = Group.objects.get_or_create(name='Alunos')
        user.groups.add(grupo_alunos)

        # 5. Mensagem de sucesso e redirecionamento
        messages.success(request, 'Cadastro realizado com sucesso! Faça seu login.')
        return redirect('login')
    
    # Se for um GET (apenas acessou a página), renderiza o formulário vazio
    return render(request, 'cadastro.html')