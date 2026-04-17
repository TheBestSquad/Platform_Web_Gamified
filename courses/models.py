from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Professor, Aluno
from accounts.models import Medalha


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
    tentativa_numero = models.PositiveIntegerField(default=1, verbose_name="Tentativa Nº")
    resposta_texto = models.TextField(verbose_name="Resposta do Aluno", blank=True)
    codigo_enviado = models.TextField(verbose_name="Código/Script", blank=True)

    # Parte do Professor
    feedback = models.TextField(verbose_name="Feedback do Professor", blank=True, null=True)
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    data_entrega = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-data_entrega']


@receiver(post_save, sender=Entrega)
def verificar_medalhas(sender, instance, **kwargs):
    # 1. Se não tem nota, para aqui
    if instance.nota is None:
        return

    # 2. Converte para float para garantir que a comparação funcione
    try:
        nota_num = float(instance.nota)
    except (ValueError, TypeError):
        return

    aluno = instance.aluno
    professor = instance.licao.professor

    # REGRA 1: Medalha de Domínio (Usando nota_num)
    if nota_num >= 10:
        Medalha.objects.get_or_create(
            aluno=aluno,
            tipo='DOMINIO',
            titulo=f"Domínio Total: {instance.licao.titulo}"
        )

    # REGRA 2: Medalha de Prática
    total_licoes = Entrega.objects.filter(aluno=aluno, licao__professor=professor).count()
    if total_licoes >= 5:
        Medalha.objects.get_or_create(
            aluno=aluno,
            tipo='PRATICA',
            titulo=f"Mão na Massa: {professor.disciplina_curso}"
        )

    # REGRA 3: Medalha de Evolução (Usando nota_num)
    entrega_anterior = Entrega.objects.filter(
        aluno=aluno,
        licao__professor=professor
    ).exclude(id=instance.id).order_by('-data_entrega').first()

    if entrega_anterior and entrega_anterior.nota is not None:
        # Comparamos o número atual com o número anterior
        if nota_num > float(entrega_anterior.nota):
            Medalha.objects.get_or_create(
                aluno=aluno,
                tipo='EVOLUCAO',
                titulo=f"Evolução: {professor.disciplina_curso}"
            )
