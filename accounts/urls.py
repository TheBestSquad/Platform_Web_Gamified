from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/professor/', views.register_professor, name='register_professor'),
    path('register/aluno/', views.register_aluno, name='register_aluno'),
    path('aprovar-aluno/<int:aluno_id>/', views.aprovar_aluno, name='aprovar_aluno'),
    path('meus-alunos/', views.lista_alunos_professor, name='lista_alunos'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),
    path('notificacoes/lidas/', views.marcar_notificacoes_lidas, name='marcar_notificacoes_lidas'),
    path('meus-professores/', views.gerenciar_professores, name='gerenciar_professores'),
]