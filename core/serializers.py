from rest_framework import serializers
from .models import Cliente, RegistroServicio


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            "nit",
            "razon_social",
            "telefono",
            "email",
            "direccion",
            "ciudad",
            "contacto",
        ]


class RegistroServicioSerializer(serializers.ModelSerializer):
    # El formulario de Angular envía el NIT; el cliente se resuelve contra el maestro.
    cliente_nit = serializers.CharField(source="cliente.nit", read_only=True)
    cliente_nombre = serializers.CharField(source="cliente.razon_social", read_only=True)
    nit = serializers.CharField(write_only=True)

    class Meta:
        model = RegistroServicio
        fields = [
            "id",
            "centro",
            "centro_beneficio",
            "pssr",
            "pedido",
            "factura",
            "tipo_doc",
            "nit",
            "cliente_nit",
            "cliente_nombre",
            "unidad",
            "marca",
            "fecha_documento",
            "fecha_entrega",
            "venta_neta",
            "gross_margin",
            "margen_porcentaje",
            "repuestos",
            "mano_obra",
            "terceros",
        ]

    def validate_nit(self, value):
        if not Cliente.objects.filter(nit=value).exists():
            raise serializers.ValidationError(
                "No existe un cliente con ese NIT en el maestro de clientes. "
                "Regístralo primero."
            )
        return value

    def create(self, validated_data):
        nit = validated_data.pop("nit")
        validated_data["cliente_id"] = nit
        return super().create(validated_data)
