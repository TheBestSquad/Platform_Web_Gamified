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
    perfil = 'aluno' if hasattr(request.user, 'aluno_profile') else 'professor'
    entregas = []
    entrega_recente = None

    # 1. Se for Aluno, busca (ou salva) a entrega
    if hasattr(request.user, 'aluno_profile'):
        aluno = request.user.aluno_profile
        entregas = Entrega.objects.filter(licao=licao, aluno=aluno).order_by('-data_entrega')
        tentativas_atuais = entregas.count()
        entrega_recente = entregas.first()

        if request.method == 'POST':
            # TRAVA 1: Se já atingiu 3 tentativas
            if tentativas_atuais >= 3:
                messages.error(request, 'Você já atingiu o limite de 3 tentativas para esta lição')
                return redirect('detalhe_licao', licao_id=licao.id)

            # TRAVA 2: Se o professor já marcou como ACERTOU na entrega anterior
            if entrega_recente and entrega_recente.acertou:
                messages.error(request, 'Você já concluiu esta lição com sucesso!')
                return redirect('detalhe_licao', licao_id=licao.id)

            # --- NOVA TRAVA 3: Aguardar Feedback ---
            # Se existe uma entrega e o campo feedback está vazio/None
            if entrega_recente and not entrega_recente.feedback:
                messages.warning(request,'Aguarde o feedback do professor sobre sua última tentativa antes de enviar uma nova.')
                return redirect('detalhe_licao', licao_id=licao.id)

            resposta = request.POST.get('resposta')

            # Salva ou atualiza a resposta
            Entrega.objects.create(
                licao=licao,
                aluno=aluno,
                resposta_texto=resposta,
                tentativa_numero=tentativas_atuais + 1,
            )
            # Redireciona para a PRÓPRIA página para evitar reenvio de formulário no F5
            messages.success(request, f'Tentativa {tentativas_atuais + 1} enviada com sucesso!')
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
        'entrega': entrega_recente,
        'perfil': perfil,
        'tentativas': entregas,
        'ultima_entrega': entrega_recente,
    })


@login_required
def lista_entregas(request):
    # Verifica se o utilizador logado é um professor
    if hasattr(request.user, 'professor_profile'):
        # Procura todas as entregas das lições que pertencem a este professor
        # Ordenamos por '-data_entrega' para que as mais recentes (Tentativa #3, por exemplo) apareçam primeiro
        entregas = Entrega.objects.filter(
            licao__professor=request.user.professor_profile
        ).order_by('-data_entrega')

        return render(request, 'courses/lista_entregas.html', {'entregas': entregas})

    # Se não for professor, redireciona para a home ou outra página
    return redirect('home')


@login_required
def dar_feedback(request, entrega_id):
    if not hasattr(request.user, 'professor_profile'):
        return redirect('home')

    entrega = get_object_or_404(Entrega, id=entrega_id)

    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        acertou_status = request.POST.get('acertou') == 'on'
        entrega.feedback = feedback
        entrega.acertou = acertou_status

        if acertou_status:
            entrega.nota = 10

        entrega.save()
        messages.success(request, f'Feedback enviado para {entrega.aluno}!')
        return redirect('lista_entregas')

    return render(request, 'courses/dar_feedback.html', {'entrega': entrega})


@login_required
def ranking(request):
    professor_id = request.GET.get('professor_id')

    if professor_id is None and hasattr(request.user, 'professor_profile'):
        professor_id = str(request.user.professor_profile.id)

    # 1. Query Base
    ranking_base = Aluno.objects.all()

    if professor_id and professor_id.isdigit():
        # Ranking por Matéria
        ranking_display = ranking_base.filter(
            minhas_entregas__licao__professor_id=professor_id
        ).annotate(
            # SOMAMOS O CAMPO 'XP' DA ENTREGA
            pontos_totais=Coalesce(Sum('minhas_entregas__xp'), Value(0))
        ).filter(pontos_totais__gt=0).order_by('-pontos_totais').distinct()

        professor = Professor.objects.filter(id=professor_id).first()
        filtro_nome = professor.disciplina_curso if professor else 'Global'
    else:
        # Ranking Global
        ranking_display = ranking_base.annotate(
            pontos_totais=Coalesce(Sum('minhas_entregas__xp'), Value(0))
        ).filter(pontos_totais__gt=0).order_by('-pontos_totais').distinct()
        filtro_nome = 'Global'

    # Hall da Fama e Posição (O restante do seu código continua igual...)
    top_5 = ranking_display[:5]

    # 4. POSIÇÃO DO ALUNO LOGADO
    minha_posicao = None
    if hasattr(request.user, 'aluno_profile'):
        meu_aluno_id = request.user.aluno_profile.id
        # Transformamos em lista apenas o necessário para performance
        for i, aluno in enumerate(ranking_display):
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