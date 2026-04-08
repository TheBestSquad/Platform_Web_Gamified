from django.db import models
from accounts.models import Professor


class Licao(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='licoes')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    link_externo = models.URLField(blank=True, null=True)
    arquivo = models.FileField(upload_to='materiais/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.professor.user.first_name}"

    class Meta:
        verbose_name = "Lição"
        verbose_name_plural = "Lições"
