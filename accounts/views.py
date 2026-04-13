from django.shortcuts import render, redirect
from .forms import ProfessorRegistrationForm, AlunoRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Professor, Aluno
from courses.models import Licao


def register_professor(request):
    if request.method == 'POST':
        form = ProfessorRegistrationForm(request.POST)
        if form.is_valid():
            # 1. Criar o User (login)
            user = User.objects.create_user(
                username=form.cleaned_data['email'], # Usando email como username
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name']
            )
            # 2. Criar o perfil do Professor ligado a esse User
            professor = form.save(commit=False)
            professor.user = user
            professor.save()
            return redirect('login') # Depois vamos criar essa URL
    else:
        form = ProfessorRegistrationForm()

    return render(request, 'accounts/register_professor.html', {'form': form})


def register_aluno(request):
    if request.method == 'POST':
        form = AlunoRegistrationForm(request.POST)
        if form.is_valid():
            # Cria o User
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name']
            )
            # Cria o Aluno (is_approved já vai como False por padrão no model)
            aluno = form.save(commit=False)
            aluno.user = user
            aluno.save()
            return redirect('login')
    else:
        form = AlunoRegistrationForm()
        
    return render(request, 'accounts/register_aluno.html', {'form': form})


@login_required
def home(request):
    # Verifica se o usuário logado é um Professor
    if hasattr(request.user, 'professor_profile'):
        professor = request.user.professor_profile
        licoes = Licao.objects.filter(professor=professor).order_by('-data_criacao')
        alunos_pendentes = Aluno.objects.filter(professor=professor, is_approved=False)
        alunos_aprovados = Aluno.objects.filter(professor=professor, is_approved=True)

        context = {
            'perfil': 'professor',
            'professor': professor,
            'licoes': licoes,
            'alunos_pendentes': alunos_pendentes,
            'alunos_aprovados': alunos_aprovados
        }
    # Verifica se o usuário logado é um Aluno
    elif hasattr(request.user, 'aluno_profile'):
        aluno = request.user.aluno_profile

        licoes = []
        entregas_feitas = []
        if aluno.is_approved:
            licoes = Licao.objects.filter(professor=aluno.professor).order_by('-data_criacao')

            from courses.models import Entrega
            entregas_feitas = Entrega.objects.filter(aluno=aluno).values_list('licao_id', flat=True)

        context = {
            'perfil': 'aluno',
            'aluno': aluno,
            'licoes': licoes,
            'entregas_feitas': entregas_feitas,
            'aprovado': aluno.is_approved
        }
    else:
        # Caso seja um Superuser que não é nem prof nem aluno
        context = {'perfil': 'admin'}

    return render(request, 'accounts/home.html', context)


@login_required
def aprovar_aluno(request, aluno_id):
    # Segurança: Só professor pode acessar essa rota
    if not hasattr(request.user, 'professor_profile'):
        return redirect('home')

    # Busca o aluno ou retorna 404 se o ID for inválido
    aluno = get_object_or_404(Aluno, id=aluno_id)

    # Segurança: O professor só pode aprovar quem é aluno DELE
    if aluno.professor == request.user.professor_profile:
        aluno.is_approved = True
        aluno.save()

    return redirect('home')