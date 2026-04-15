from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from .forms import LicaoForm
from .models import Licao, Entrega
from accounts.models import Aluno, Professor


@login_required
def criar_licao(request):
    # Segurança: Apenas professores podem postar
    if not hasattr(request.user, 'professor_profile'):
        return redirect('home')

    if request.method == 'POST':
        # Importante: request.FILES é necessário para processar uploads de arquivos!
        form = LicaoForm(request.POST, request.FILES)
        if form.is_valid():
            licao = form.save(commit=False)
            licao.professor = request.user.professor_profile
            licao.save()
            messages.success(request, 'Lição publicada com sucesso! 🚀')
            return redirect('home')
    else:
        form = LicaoForm()

    return render(request, 'courses/criar_licao.html', {'form': form})


@login_required
def detalhe_licao(request, licao_id):
    licao = get_object_or_404(Licao, id=licao_id)
    entrega = None
    perfil = 'aluno' if hasattr(request.user, 'aluno_profile') else 'professor'

    # 1. Se for Aluno, busca (ou salva) a entrega
    if hasattr(request.user, 'aluno_profile'):
        aluno = request.user.aluno_profile
        entrega = Entrega.objects.filter(licao=licao, aluno=aluno).first()

        if request.method == 'POST':
            if entrega:
                return redirect('detalhe_licao', licao_id=licao.id)

            resposta = request.POST.get('resposta')
            codigo = request.POST.get('codigo')

            # Salva ou atualiza a resposta
            Entrega.objects.update_or_create(
                licao=licao,
                aluno=aluno,
                resposta_texto=resposta,
                codigo_enviado=codigo,
            )
            # Redireciona para a PRÓPRIA página para evitar reenvio de formulário no F5
            messages.success(request, 'Sua resposta foi enviada com sucesso! Agora é só aguardar a correção. 😉')
            return redirect('home')

    # 2. Se for Professor, ele apenas visualiza (não entra no POST de aluno)
    elif hasattr(request.user, 'professor_profile'):
        # Professor pode querer ver a entrega de um aluno específico futuramente,
        # mas por enquanto ele só vê a lição "seca" ou a entrega via admin.
        pass

    # 3. Se não for nenhum dos dois perfis (ex: Superuser), manda para a home real
    else:
        # Verifique se o nome da sua URL da home é realmente 'home' no core/urls.py
        return redirect('home')

    return render(request, 'courses/detalhe_licao.html', {
        'licao': licao,
        'entrega': entrega,
        'perfil': perfil,
    })


@login_required
def lista_entregas(request):
    if not hasattr(request.user, 'professor_profile'):
        return redirect('home')

    # Busca todas as entregas feitas para as lições deste professor
    entregas = Entrega.objects.filter(licao__professor=request.user.professor_profile).order_by('-data_entrega')

    return render(request, 'courses/lista_entregas.html', {'entregas': entregas})


@login_required
def dar_feedback(request, entrega_id):
    if not hasattr(request.user, 'professor_profile'):
        return redirect('home')

    entrega = get_object_or_404(Entrega, id=entrega_id, licao__professor=request.user.professor_profile)

    if request.method == 'POST':
        entrega.feedback = request.POST.get('feedback')
        entrega.nota = request.POST.get('nota')
        entrega.save()
        return redirect('lista_entregas')

    return render(request, 'courses/dar_feedback.html', {'entrega': entrega})


@login_required
def ranking(request):
    professor_id = request.GET.get('professor_id')

    # Lógica de prioridade para Professor
    if professor_id is None and hasattr(request.user, 'professor_profile'):
        professor_id = str(request.user.professor_profile.id)

    # 1. Query Base: Todos os alunos com a soma de XP
    ranking_geral = Aluno.objects.annotate(
        pontos_totais=Coalesce(Sum('minhas_entregas__nota'), Value(0), output_field=DecimalField())
    ).order_by('-pontos_totais')

    # 2. Filtragem por Professor (se houver)
    if professor_id and professor_id.isdigit():
        ranking_display = ranking_geral.filter(
            minhas_entregas__licao__professor_id=professor_id
        ).filter(pontos_totais__gt=0)
        professor = Professor.objects.filter(id=professor_id).first()
        filtro_nome = professor.disciplina_curso if professor else 'Global'
    else:
        ranking_display = ranking_geral.filter(pontos_totais__gt=0)
        filtro_nome = 'Global'

    # 3. HALL DA FAMA: Apenas o Top 5
    top_5 = ranking_display[:5]

    # 4. POSIÇÃO DO ALUNO LOGADO:
    # Procuramos o aluno na lista completa do ranking atual
    minha_posicao = None
    if hasattr(request.user, 'aluno_profile'):
        meu_aluno_id = request.user.aluno_profile.id
        # Convertemos para lista para achar o índice
        lista_ranking = list(ranking_display)
        for i, aluno in enumerate(lista_ranking):
            if aluno.id == meu_aluno_id:
                minha_posicao = i + 1
                break

    context = {
        'top_5': top_5,
        'minha_posicao': minha_posicao,
        'todos_professores': Professor.objects.all(),
        'filtro_nome': filtro_nome,
        'professor_selecionado': int(professor_id) if professor_id and professor_id.isdigit() else None
    }
    return render(request, 'courses/ranking.html', context)