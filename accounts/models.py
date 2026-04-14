from django.db import models
from django.contrib.auth.models import User


class Professor(models.Model):
    # O OneToOneField liga o perfil a um usuário do sistema (que tem login e senha)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')
    formacao = models.CharField(max_length=255)
    contato = models.CharField(max_length=100)
    disciplina_curso = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='perfil_fotos/', null=True, blank=True)

    def __str__(self):
        return f'Professor {self.user.first_name} {self.user.last_name} - {self.disciplina_curso}'


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno_profile')
    contato = models.CharField(max_length=20)
    professores = models.ManyToManyField(Professor, through='Matricula', related_name='alunos')
    # Status para aprovação manual do professor
    is_approved = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='perfil_fotos/', null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    data_vinculo = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False) # Agora a aprovação é POR professor

    class Meta:
        unique_together = ('aluno', 'professor')