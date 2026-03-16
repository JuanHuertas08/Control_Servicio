from django.contrib import admin
from .models import Seguimiento

@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
   list_display = ('Id', 'Cliente', 'Factura', 'Tipo_Facturacion', 'PSSR', 'Fecha_Facturacion', 'ESTADO','Fecha_Seguimiento','Tipo_Contacto', 'Observaciones')