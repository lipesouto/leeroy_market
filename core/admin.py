# core/admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ship, Pedido

class MyAdminSite(admin.AdminSite):
    site_header = "EVE Admin"
    site_title = "EVE Admin"
    index_title = "Painel EVE"

    def has_permission(self, request):
        return request.user.is_active

admin_site = MyAdminSite(name='myadmin')

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

admin_site.register(Pedido)

