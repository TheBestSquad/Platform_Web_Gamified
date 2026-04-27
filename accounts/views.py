from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfessorRegistrationForm, AlunoRegistrationForm, UserUpdateForm, ProfessorUpdateForm, AlunoUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import Professor, Aluno, Matricula, Notificacao
from courses.models import Licao, Entrega


def register_professor(request):
<<<<<<< HEAD
    """
    Realiza o cadastro de um novo professor no sistema.

    Cria simultaneamente um objeto User (autenticação) e um perfil de Professor.
    O e-mail fornecido é utilizado como nome de usuário para o login.
    """
=======
>>>>>>> 25e2af42ce260e5c0305aadbfbd126686def07fb
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
<<<<<<< HEAD
    """
    Realiza o cadastro de um novo aluno no sistema.

    Assim como no professor, cria o User e o perfil de Aluno.
    O aluno inicia com o status is_approved=False, aguardando aprovação
    dos professores selecionados no formulário (save_m2m).
    """
=======
>>>>>>> 25e2af42ce260e5c0305aadbfbd126686def07fb
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
<<<<<<< HEAD
    """
    View principal (Dashboard) que redireciona a lógica conforme o tipo de usuário.

    - Professores: Visualizam suas lições criadas e solicitações de matrícula.
    - Alunos: Visualizam seu progresso (XP, Nível), barra de progresso calculada
    e a lista de lições dos professores que já aprovaram seu vínculo.
    """
=======
>>>>>>> 25e2af42ce260e5c0305aadbfbd126686def07fb
    context = {}

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
        from django.db.models import Sum, Count

        # 1. XP Total Real
        xp_total = Entrega.objects.filter(aluno=aluno).aggregate(total=Sum('xp'))['total'] or 0

        # --- LÓGICA DA BARRA DE PROGRESSO POR NÍVEL ---
        if xp_total < 100:
            nome_nivel = "Iniciante"
            cor_nivel = "text-slate-400"
            proximo_xp = 100
            # No primeiro nível, a barra é direta (0 a 100)
            progresso_barra = xp_total
        elif xp_total < 500:
            nome_nivel = "Intermediário"
            cor_nivel = "text-blue-500"
            proximo_xp = 500
            # Cálculo: (XP atual - XP que já passou) / (XP do nível atual)
            progresso_barra = ((xp_total - 100) / (500 - 100)) * 100
        else:
            nome_nivel = "Avançado"
            cor_nivel = "text-yellow-500"
            proximo_xp = 1000
            progresso_barra = ((xp_total - 500) / (1000 - 500)) * 100

        # 2. Lições que o aluno já tocou (qualquer tentativa)
        entregas_feitas = Entrega.objects.filter(aluno=aluno).values_list('licao_id', flat=True)

        # 3. Lições que ele ACERTOU
        licoes_acertadas = Entrega.objects.filter(aluno=aluno, acertou=True).values_list('licao_id', flat=True)

        # 4. Lições onde ele ESGOTOU as 3 tentativas
        licoes_esgotadas = Entrega.objects.filter(aluno=aluno).values('licao_id').annotate(
            total_tentativas=Count('id')
        ).filter(total_tentativas__gte=3).values_list('licao_id', flat=True)

        # Unir os IDs de lições finalizadas para o botão ficar verde
        licoes_finalizadas = set(list(licoes_acertadas) + list(licoes_esgotadas))

        licoes_por_professor = {}
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
            'licoes_finalizadas': licoes_finalizadas,
            'xp_total': xp_total,
            'progresso_barra': progresso_barra,
            'proximo_xp': proximo_xp,
            'nome_nivel': nome_nivel,
            'cor_nivel': cor_nivel,
        }

    # 3. Lógica para Admin/Outros
    else:
        context = {'perfil': 'admin'}

    return render(request, 'accounts/home.html', context)


@login_required
def aprovar_aluno(request, aluno_id):
<<<<<<< HEAD
    """
    Aprova a matrícula de um aluno para o professor logado.

    Muda o status da relação na tabela Matricula para is_approved=True,
    permitindo que o aluno visualize o conteúdo deste professor.
    """
=======
>>>>>>> 25e2af42ce260e5c0305aadbfbd126686def07fb
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
<<<<<<< HEAD
    """
    Exibe a listagem de todos os alunos vinculados e aprovados do professor logado.

    Utiliza select_related para otimizar a consulta ao banco de dados.
    """
=======
>>>>>>> 25e2af42ce260e5c0305aadbfbd126686def07fb
    professor = request.user.professor_profile
    from .models import Matricula  # Garanta que o import está aqui

    # Buscamos as MATRÍCULAS aprovadas deste professor específico
    matriculas = Matricula.objects.filter(
        professor=professor,
        is_approved=True
    ).select_related('aluno__user')  # Otimiza a busca dos nomes

    return render(request, 'accounts/lista_alunos.html', {
        'matriculas': matriculas, # Mudamos o nome da variável para facilitar no HTML
        'total_alunos': matriculas.count(),
    })

@login_required
def editar_perfil(request):
<<<<<<< HEAD
    """
    Gerencia a atualização dos dados cadastrais e fotos de perfil.

    Identifica automaticamente o tipo de perfil (Aluno ou Professor)
    e carrega os formulários correspondentes.
    """
=======
>>>>>>> 25e2af42ce260e5c0305aadbfbd126686def07fb
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


@login_required
def marcar_notificacoes_lidas(request):
<<<<<<< HEAD
    """
    Marca todas as notificações pendentes do usuário logado como lidas.

    Redireciona para a página anterior após a atualização.
    """
=======
>>>>>>> 25e2af42ce260e5c0305aadbfbd126686def07fb
    # Filtra todas as notificações do usuário logado que ainda não foram lidas e as marca como True
    Notificacao.objects.filter(user=request.user, lida=False).update(lida=True)

    # Redireciona o usuário de volta para a página onde ele estava
    return redirect(request.META.get('HTTP_REFERER', 'home'))