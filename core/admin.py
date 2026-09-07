from django.contrib import admin
from .models import Cliente, RegistroServicio


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nit", "razon_social", "telefono", "email", "ciudad")
    search_fields = ("nit", "razon_social")


@admin.register(RegistroServicio)
class RegistroServicioAdmin(admin.ModelAdmin):
    list_display = ("pedido", "cliente", "factura", "fecha_documento", "venta_neta")
    search_fields = ("pedido", "factura", "cliente__nit", "cliente__razon_social")
    autocomplete_fields = ("cliente",)
