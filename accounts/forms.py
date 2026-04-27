from django import forms
from django.contrib.auth.models import User
from .models import Professor, Aluno


class ProfessorRegistrationForm(forms.ModelForm):
    """
    Formulário para cadastro inicial de Professores.

    Combina campos de autenticação (User) com campos de perfil profissional.
    Inclui validação de confirmação de senha.
    """
    # Campos do User
    first_name = forms.CharField(label="Nome Completo", max_length=150)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    class Meta:
        model = Professor
        fields = ['formacao', 'contato', 'disciplina_curso', 'foto']

    def clean(self):
        """
        Verifica se os campos de senha e confirmação de senha são idênticos.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem!")
        return cleaned_data


class AlunoRegistrationForm(forms.ModelForm):
    """
    Formulário para cadastro inicial de Alunos.

    Permite que o aluno escolha múltiplos professores/matérias no ato do cadastro.
    A relação ManyToMany é gerenciada através de um CheckboxSelectMultiple.
    """
    # Campos do User
    first_name = forms.CharField(label="Nome Completo", max_length=150)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    # Campo para selecionar o professor (vai vir do banco)
    professores = forms.ModelMultipleChoiceField(
        queryset=Professor.objects.all(),
        label="Selecione seus Professores / Matérias",
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Aluno
        fields = ['contato', 'professores', 'foto']

    def clean(self):
        """
        Valida a integridade das senhas fornecidas pelo aluno.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem!")
        return cleaned_data


# Formulário para dados básicos do User
class UserUpdateForm(forms.ModelForm):
    """
    Formulário para atualização de dados de autenticação comuns a qualquer usuário.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Formulário para dados extras do Professor
class ProfessorUpdateForm(forms.ModelForm):
    """
    Formulário para edição dos dados profissionais do Professor.
    """
    class Meta:
        model = Professor
        fields = ['formacao', 'contato', 'disciplina_curso', 'foto']

# Formulário para dados extras do Aluno
class AlunoUpdateForm(forms.ModelForm):
    """
    Formulário para edição dos dados de contato e foto do Aluno.
    """
    class Meta:
        model = Aluno
        fields = ['contato', 'foto']