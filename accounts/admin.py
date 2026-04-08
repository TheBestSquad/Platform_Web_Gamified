from django.contrib import admin
from .models import Professor, Aluno


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'disciplina_curso', 'formacao')

    def get_name(self, obj):
        return obj.user.get_full_name()

    get_name.short_description = 'Nome'


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'professor', 'is_approved')
    list_filter = ('is_approved', 'professor')  # Filtros na lateral
    list_editable = ('is_approved',)  # Permite aprovar direto na lista

    def get_name(self, obj):
        return obj.user.get_full_name()

    get_name.short_description = 'Nome'

