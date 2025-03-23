from django.db import models

# core/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class ShipCategory(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'ship_categories'
        managed = False

    def __str__(self):
        return self.category_name


class Ship(models.Model):
    ship_name = models.CharField(max_length=100)
    category = models.ForeignKey(
        ShipCategory,
        on_delete=models.CASCADE,
        db_column='category_id',
        related_name='ships'
    )

    class Meta:
        db_table = 'ships'
        managed = False

    def __str__(self):
        return self.ship_name

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nave = models.ForeignKey(Ship, on_delete=models.CASCADE)  # Troque "Nave" por "Ship"
    status = models.CharField(max_length=50, default="Pendente")
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.nave} - {self.status}"


class EveProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='eve_profile')
    character_id = models.CharField(max_length=20)
    character_name = models.CharField(max_length=100)
    portrait_url = models.URLField(blank=True, null=True)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    token_expires = models.DateTimeField(blank=True, null=True)  # quando expira o access_token (opcional)
    # Outros campos que você queira armazenar (corporação, alliance, etc.)

    def __str__(self):
        return self.character_name
