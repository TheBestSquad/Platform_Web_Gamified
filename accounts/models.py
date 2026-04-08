from django.db import models
from django.contrib.auth.models import User


class Professor(models.Model):
    # O OneToOneField liga o perfil a um usuário do sistema (que tem login e senha)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')
    formacao = models.CharField(max_length=255)
    contato = models.CharField(max_length=100)
    disciplina_curso = models.CharField(max_length=255)

    def __str__(self):
        return f'Professor {self.user.first_name} {self.user.last_name} - {self.disciplina_curso}'


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno_profile')
    contato = models.CharField(max_length=20)
    # Aqui o aluno escolhe o professor no cadastro
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, related_name='alunos')
    # Status para aprovação manual do professor
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()