from .models import Notificacao

def notificacoes_usuario(request):
    if request.user.is_authenticated:
        return {
            'notificacoes_recentes': Notificacao.objects.filter(user=request.user, lida=False)[:5],
            'contador_notificacoes': Notificacao.objects.filter(user=request.user, lida=False).count()
        }
    return {}