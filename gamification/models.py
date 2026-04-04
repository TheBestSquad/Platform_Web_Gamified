from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    # Campos customizados adicionais
    data_nascimento = models.DateField(null=True, blank=True)
    instituicao = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.email or self.username