from django.contrib import admin
from .models import Licao, Entrega


@admin.register(Licao)
class LicaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'professor', 'data_criacao')
    search_fields = ('titulo', 'professor__user__first_name')

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('licao', 'aluno', 'nota', 'data_entrega')
    list_filter = ('licao__professor', 'data_entrega')
    # Isso ajuda muito a encontrar entregas específicas
    search_fields = ('aluno__user__first_name', 'licao__titulo')
