from django.urls import path
from . import views

urlpatterns = [
    path('register/professor/', views.register_professor, name='register_professor'),
]