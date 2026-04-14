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
    list_display = ('get_name', 'get_professores', 'is_approved')
    list_filter = ('is_approved',)  # Filtros na lateral
    list_editable = ('is_approved',)  # Permite aprovar direto na lista

    def get_name(self, obj):
        return obj.user.get_full_name()

    get_name.short_description = 'Nome'

    def get_professores(self, obj):
        return ", ".join([p.user.first_name for p in obj.professores.all()])
    get_professores.short_description = 'Professores/Matérias'

