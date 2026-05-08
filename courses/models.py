from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Professor, Aluno
from accounts.models import Medalha


class Licao(models.Model):
    """
    Representa o conteúdo pedagógico postado pelo professor.

    Armazena o material de estudo, as questões a serem respondidas e
    suporte para arquivos ou links externos.
    """
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
    """
    Representa a resposta de um aluno a uma lição específica.

    Gerencia o ciclo de vida da atividade, desde o envio da resposta
    pelo aluno até o feedback, atribuição de nota e cálculo de XP pelo professor.
    """
    licao = models.ForeignKey(Licao, on_delete=models.CASCADE, related_name='entregas')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='minhas_entregas')
    tentativa_numero = models.PositiveIntegerField(default=1, verbose_name="Tentativa Nº")
    resposta_texto = models.TextField(verbose_name="Resposta do Aluno", blank=True)

    # Parte do Professor
    feedback = models.TextField(verbose_name="Feedback do Professor", blank=True, null=True)
    nota = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    acertou = models.BooleanField(default=False, verbose_name="O aluno acertou?")

    xp = models.IntegerField(default=0, editable=False)
    data_entrega = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['-data_entrega']

    def save(self, *args, **kwargs):
        """
        Sobrescreve o processo save para calcular o XP automaticamente.

        Lógica de XP:
            - 1ª tentativa: 10 XP base.
            - Tentativas posteriores: 15 XP base.
            - Se o professor marcar 'acertou', garante nota 10 e mínimo de 15 XP.
        """
        # 1. Define o XP base no momento do envio (criação)
        if not self.pk:
            # Define o XP fixo baseado na tentativa no momento do envio
            if self.tentativa_numero == 1:
                self.xp = 15
            elif self.tentativa_numero == 2:
                self.xp = 10
            else:
                self.xp = 5

        # Se o professor marcar que acertou, garantimos que a nota seja 10 (opcional, mas ajuda)
        if self.acertou:
            self.nota = 10.00
            self.xp += 15

        super().save(*args, **kwargs)

    def __str__(self):
        status = "ACERTOU" if self.acertou else "ERROU/PENDENTE"
        return f"{self.aluno.user.username} - {self.licao.titulo} (T#{self.tentativa_numero}) - {status}"

@receiver(post_save, sender=Entrega)
def verificar_medalhas(sender, instance, **kwargs):
    """
    Signal que verifica e atribui medalhas após a gravação de uma Entrega.

    Regras de Negócio:
        - DOMÍNIO: Atribuída se a nota for maior ou igual a 10.
        - PRÁTICA: Atribuída se o aluno completar 5 ou mais lições do mesmo professor.
        - EVOLUÇÃO: Atribuída se a nota atual for maior que a nota da entrega anterior.
    """
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
