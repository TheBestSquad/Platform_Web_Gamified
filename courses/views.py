from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LicaoForm


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