from django.urls import path
from . import views

urlpatterns = [
    path('postar/', views.criar_licao, name='criar_licao'),
    path('licao/<int:licao_id>/', views.detalhe_licao, name='detalhe_licao'),
]