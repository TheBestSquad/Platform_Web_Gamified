from django import forms
from .models import Licao

class LicaoForm(forms.ModelForm):
    class Meta:
        model = Licao
        fields = ['titulo', 'descricao', 'questoes', 'link_externo', 'arquivo']
        # Adicionamos classes do Tailwind aqui para facilitar a renderização
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'w-full border rounded p-2 outline-none focus:ring-2 focus:ring-blue-500'}),
            'descricao': forms.Textarea(attrs={'class': 'w-full border rounded p-2 outline-none focus:ring-2 focus:ring-blue-500', 'rows': 4}),
            'questoes': forms.Textarea(
                attrs={'class': 'w-full border rounded p-2 outline-none focus:ring-2 focus:ring-blue-500', 'rows': 4,
                       'placeholder': 'Digite as perguntas aqui...'}),
            'link_externo': forms.URLInput(attrs={'class': 'w-full border rounded p-2 outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'https://...'}),
            'arquivo': forms.FileInput(attrs={'class': 'w-full border p-1 text-gray-700'}),
        }