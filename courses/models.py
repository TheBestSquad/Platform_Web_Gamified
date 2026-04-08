from django.db import models
from accounts.models import Professor, Aluno


class Licao(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='licoes')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    questoes = models.TextField(verbose_name="Questões da Lição", blank=True, null=True)
    link_externo = models.URLField(blank=True, null=True)
    arquivo = models.FileField(upload_to='materiais/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.professor.user.first_name}"

    class Meta:
        verbose_name = "Lição"
        verbose_name_plural = "Lições"


class Entrega(models.Model):
    licao = models.ForeignKey(Licao, on_delete=models.CASCADE, related_name='entregas')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='minhas_entregas')
    resposta_texto = models.TextField(verbose_name="Resposta do Aluno", blank=True)
    codigo_enviado = models.TextField(verbose_name="Código/Script", blank=True)

    # Parte do Professor
    feedback = models.TextField(verbose_name="Feedback do Professor", blank=True, null=True)
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    data_entrega = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que o aluno só entregue uma vez por lição (opcional)
        unique_together = ['licao', 'aluno']