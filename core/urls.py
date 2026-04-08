from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # Adiciona as rotas padrão do Django (login, logout, password_reset)
    path('accounts/', include('django.contrib.auth.urls')),
]
