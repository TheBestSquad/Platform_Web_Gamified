from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Adiciona os novos campos ao painel de edição do admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Educacionais', {'fields': ('data_nascimento', 'instituicao')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)