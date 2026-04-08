from django import forms
from django.contrib.auth.models import User
from .models import Professor

class ProfessorRegistrationForm(forms.ModelForm):
    # Campos do User
    first_name = forms.CharField(label="Nome Completo", max_length=150)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    class Meta:
        model = Professor
        fields = ['formacao', 'contato', 'disciplina_curso']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem!")
        return cleaned_data