from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import LicaoForm
from .models import Licao, Entrega
from accounts.models import Aluno


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
            resposta = request.POST.get('resposta')
            codigo = request.POST.get('codigo')

            # Salva ou atualiza a resposta
            Entrega.objects.update_or_create(
                licao=licao,
                aluno=aluno,
                defaults={'resposta_texto': resposta, 'codigo_enviado': codigo}
            )
            # Redireciona para a PRÓPRIA página para evitar reenvio de formulário no F5
            return redirect('detalhe_licao', licao_id=licao.id)

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
    # Pegamos todos os alunos, somamos as notas das suas entregas
    # e ordenamos do maior para o menor.
    ranking_list = Aluno.objects.annotate(
        pontos_totais=Sum('minhas_entregas__nota')
    ).filter(pontos_totais__isnull=False).order_by('-pontos_totais')

    return render(request, 'courses/ranking.html', {'ranking': ranking_list})