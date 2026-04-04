"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# Importações para o template de login
from django.contrib.auth import views as auth_views
from gamification.views import home_view
# Importações necessárias para o redirecionamento do favicon.ico
from django.views.generic.base import RedirectView, TemplateView
from django.conf import settings

urlpatterns = [
    # Rota de login nativa do Django apontando para o template personalizado
    path('login/', auth_views.LoginView.as_view(
        template_name='login.html', 
        redirect_authenticated_user=True
    ), name='login'),
    # Rota para a página principal
    path('', home_view, name='home'),
    # Rota para a interface de administração do Django
    path('admin/', admin.site.urls),

    # Redireciona a busca automática do navegador pelo ícone para o diretório de estáticos (evita erro de favicon.ico not fount)
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico', permanent=True)),
]
