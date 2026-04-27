from django.contrib import admin
from .models import Licao, Entrega


@admin.register(Licao)
class LicaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'professor', 'data_criacao')
    search_fields = ('titulo', 'professor__user__first_name')


@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'licao', 'tentativa_numero', 'data_entrega')
    list_filter = ('licao', 'aluno', 'tentativa_numero')
    search_fields = ('aluno__user__first_name', 'aluno__user__last_name', 'licao__titulo')
    ordering = ('-data_entrega',)
