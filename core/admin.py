# core/admin.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Ship, Pedido

# Importa User e Group do Django Auth
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin, GroupAdmin

class MyAdminSite(admin.AdminSite):
    site_header = "EVE Admin"
    site_title = "EVE Admin"
    index_title = "Painel EVE"

    # Define que qualquer usuário ativo pode acessar este admin
    # (Se quiser restringir somente a staff, use request.user.is_staff)
    def has_permission(self, request):
        return request.user.is_active

# Instancia o admin customizado
admin_site = MyAdminSite(name='myadmin')

# Exemplo de ModelAdmin para Ship, se quiser exibir no admin
class NaveAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_active

    def has_view_permission(self, request, obj=None):
        return request.user.is_active

    def has_add_permission(self, request):
        return request.user.is_active

    def has_change_permission(self, request, obj=None):
        return request.user.is_active

    def has_delete_permission(self, request, obj=None):
        return request.user.is_active

# Registra o modelo Ship (se desejar exibir naves no admin)
# admin_site.register(Ship, NaveAdmin)

# Registra o modelo Pedido
admin_site.register(Pedido)

# Registra User e Group no admin customizado
admin_site.register(User, AuthUserAdmin)
admin_site.register(Group, GroupAdmin)
