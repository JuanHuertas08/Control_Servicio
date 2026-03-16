from rest_framework import serializers
from .models import Seguimiento

class SeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento
        fields = [
            'Id', 
            'Cliente', 
            'Factura', 
            'Tipo_Facturacion', 
            'PSSR', 
            'Fecha_Facturacion', 
            'ESTADO', 
            'Fecha_Seguimiento', 
            'Tipo_Contacto', 
            'Observaciones'
        ]