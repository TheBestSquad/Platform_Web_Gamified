from django.contrib import admin
from .models import Professor, Aluno, Medalha, Matricula, Notificacao


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


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'professor', 'is_approved', 'data_vinculo')
    list_filter = ('is_approved', 'professor')
    list_editable = ('is_approved',)


@admin.register(Medalha)
class MedalhaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'aluno', 'tipo', 'data_conquista')
    list_filter = ('tipo', 'data_conquista')
    search_fields = ('aluno__user__first_name', 'titulo')


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('user', 'mensagem', 'data_criacao', 'lida')
    list_filter = ('lida', 'data_criacao')
    serach_fields = ('user__username', 'mensagem')


