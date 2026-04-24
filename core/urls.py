from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name='home'),
    path('accounts/', include('accounts.urls')),
    # Adiciona as rotas padrão do Django (login, logout, password_reset)
    path('accounts/', include('django.contrib.auth.urls')),
    path('courses/', include('courses.urls')),

    # Password Reset URLs
    path('reset-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-senha/enviado/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset-senha/concluido/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
