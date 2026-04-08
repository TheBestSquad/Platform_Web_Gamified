from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import LicaoForm
from .models import Licao, Entrega


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

    if hasattr(request.user, 'aluno_profile'):
        entrega = Entrega.objects.filter(licao=licao, aluno=request.user.aluno_profile).first()

        if request.method == 'POST':
            # Lógica para salvar a resposta do aluno
            resposta = request.POST.get('resposta')
            codigo = request.POST.get('codigo')

            Entrega.objects.update_or_create(
                licao=licao,
                aluno=request.user.aluno_profile,
                defaults={'resposta_texto': resposta, 'codigo_enviado': codigo}
            )
        return redirect('detalhe_licao', licao_id=licao.id)

    return render(request, 'courses/detalhe_licao.html', {
        'licao': licao,
        'entrega': entrega
    })