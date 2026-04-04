from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Bloquear o acesso de quem não estiver logado.
@login_required 
def home_view(request):
    return render(request, 'home.html')