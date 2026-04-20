from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfessorRegistrationForm, AlunoRegistrationForm, UserUpdateForm, ProfessorUpdateForm, AlunoUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Professor, Aluno, Matricula
from courses.models import Licao, Entrega


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

            form.save_m2m()
            messages.success(request, "Cadastro realizado com sucesso! Aguarde a aprovação dos seus professores.")
            return redirect('login')
    else:
        form = AlunoRegistrationForm()
        
    return render(request, 'accounts/register_aluno.html', {'form': form})


@login_required
def home(request):
    context = {}  # Criamos um contexto vazio para garantir que algo sempre seja enviado

    # 1. Lógica para Professor
    if hasattr(request.user, 'professor_profile'):
        professor = request.user.professor_profile
        from .models import Matricula
        from courses.models import Licao

        context = {
            'perfil': 'professor',
            'professor': professor,
            'licoes': Licao.objects.filter(professor=professor).order_by('-data_criacao'),
            'matriculas_pendentes': Matricula.objects.filter(professor=professor, is_approved=False),
            'matriculas_aprovadas': Matricula.objects.filter(professor=professor, is_approved=True)
        }

    # 2. Lógica para Aluno
    elif hasattr(request.user, 'aluno_profile'):
        aluno = request.user.aluno_profile
        from .models import Matricula
        from courses.models import Licao, Entrega
        from django.db.models import Sum

        xp_total = Entrega.objects.filter(aluno=aluno).aggregate(total=Sum('xp'))['total'] or 0

        licoes_por_professor = {}
        entregas_feitas = Entrega.objects.filter(aluno=aluno).values_list('licao_id', flat=True)

        # Buscamos apenas as lições dos professores que já APROVARAM esse aluno
        matriculas_ativas = Matricula.objects.filter(aluno=aluno, is_approved=True)

        for matricula in matriculas_ativas:
            licoes = Licao.objects.filter(professor=matricula.professor).order_by('-data_criacao')
            if licoes.exists():
                licoes_por_professor[matricula.professor] = licoes

        context = {
            'perfil': 'aluno',
            'aluno': aluno,
            'licoes_por_professor': licoes_por_professor,
            'entregas_feitas': entregas_feitas,
            'xp_total': xp_total,
        }

    # 3. Lógica para Admin/Outros
    else:
        context = {'perfil': 'admin'}

    # O RETURN DEVE FICAR AQUI, FORA DE TODOS OS IFs
    return render(request, 'accounts/home.html', context)


@login_required
def aprovar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    professor_logado = request.user.professor_profile

    # Busca a matrícula específica desse aluno com esse professor
    matricula = Matricula.objects.get(aluno=aluno, professor=professor_logado)
    matricula.is_approved = True
    matricula.save()

    messages.success(request, f'Você aprovou {aluno.user.first_name} na sua disciplina!')
    return redirect('home')


@login_required
def lista_alunos_professor(request):
    professor = request.user.professor_profile
    from .models import Matricula  # Garanta que o import está aqui

    # Buscamos as MATRÍCULAS aprovadas deste professor específico
    matriculas = Matricula.objects.filter(
        professor=professor,
        is_approved=True
    ).select_related('aluno__user')  # Otimiza a busca dos nomes

    return render(request, 'accounts/lista_alunos.html', {
        'matriculas': matriculas  # Mudamos o nome da variável para facilitar no HTML
    })

@login_required
def editar_perfil(request):
    # Identifica qual é o perfil do usuário logado
    if hasattr(request.user, 'professor_profile'):
        perfil = request.user.professor_profile
        perfil_form_class = ProfessorUpdateForm
    else:
        perfil = request.user.aluno_profile
        perfil_form_class = AlunoUpdateForm

    if request.method == 'POST':
        # Instancia os dois formulários com os dados enviados
        user_form = UserUpdateForm(request.POST, instance=request.user)
        # O request.FILES é obrigatório para salvar a foto!
        perfil_form = perfil_form_class(request.POST, request.FILES, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('editar_perfil')
    else:
        user_form = UserUpdateForm(instance=request.user)
        perfil_form = perfil_form_class(instance=perfil)

    return render(request, 'accounts/editar_perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form, # Passamos o form de perfil para o template
        'perfil': perfil
    })