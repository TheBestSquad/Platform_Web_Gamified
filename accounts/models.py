from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce


class Professor(models.Model):
    # O OneToOneField liga o perfil a um usuário do sistema (que tem login e senha)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')
    formacao = models.CharField(max_length=255)
    contato = models.CharField(max_length=100)
    disciplina_curso = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='perfil_fotos/', null=True, blank=True)

    def __str__(self):
        return f'Professor {self.user.first_name} {self.user.last_name} - {self.disciplina_curso}'

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aluno_profile')
    contato = models.CharField(max_length=20)
    professores = models.ManyToManyField(Professor, through='Matricula', related_name='alunos')
    # Status para aprovação manual do professor
    is_approved = models.BooleanField(default=False)
    foto = models.ImageField(upload_to='perfil_fotos/', null=True, blank=True)

    @property
    def xp_total(self):
        entregas = self.minhas_entregas.all()
        total_xp = 0
        for entrega in entregas:
            if entrega.tentativa_numero == 1:
                total_xp += 10
            elif entrega.tentativa_numero in [2, 3]:
                total_xp += 15
        return total_xp

    @property
    def nivel_info(self):
        xp = self.xp_total
        # Definição das faixas (ajuste conforme o grupo preferir)
        if xp < 100:
            return {'nome': 'Iniciante', 'cor': 'text-slate-400', 'proximo': 100, 'min': 0}
        elif xp < 500:
            return {'nome': 'Intermediário', 'cor': 'text-blue-500', 'proximo': 500, 'min': 100}
        else:
            return {'nome': 'Avançado', 'cor': 'text-purple-600', 'proximo': 1500, 'min': 500}

    @property
    def progresso_nivel(self):
        info = self.nivel_info
        xp_atual = self.xp_total

        # Cálculo da porcentagem dentro do nível atual
        total_do_nivel = info['proximo'] - info['min']
        progresso_no_nivel = xp_atual - info['min']

        if total_do_nivel <= 0: return 100

        porcentagem = (progresso_no_nivel / total_do_nivel) * 100
        return min(max(porcentagem, 0), 100)  # Garante que fique entre 0 e 100

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'


class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    data_vinculo = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False) # Agora a aprovação é POR professor

    class Meta:
        unique_together = ('aluno', 'professor')
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'


class Medalha(models.Model):
    TIPOS = [
        ('DOMINIO', 'Domínio Total'),  # Para quem tirou 100
        ('PRATICA', 'Mão na Massa'),  # Para quem completou tudo
        ('EVOLUCAO', 'Evolução Constante'),  # Para melhora de desempenho
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='minhas_medalhas')
    tipo = models.CharField(max_length=20, choices=TIPOS)
    titulo = models.CharField(max_length=100)  # Ex: "Mestre de Python" ou "Evoluiu 20%"
    data_conquista = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.aluno.user.first_name}"

    class Meta:
        verbose_name = 'Medalha'
        verbose_name_plural = 'Medalhas'


class Notificacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacao')
    mensagem = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return f'Notificação para {self.user.username}: {self.mensagem}'


