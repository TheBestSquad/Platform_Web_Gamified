from django.urls import path
from . import views

urlpatterns = [
    path('postar/', views.criar_licao, name='criar_licao'),
]