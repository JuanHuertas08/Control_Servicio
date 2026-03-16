from django.db import models

class RegistroServicio(models.Model):
    # Datos de Ubicación y Responsables
    centro = models.CharField("Centro", max_length=20)
    centro_beneficio = models.CharField("C. Beneficio", max_length=50)
    pssr = models.CharField("PSSR / Asesor", max_length=100)
    
    # Identificación del Documento
    pedido = models.BigIntegerField("Pedido", unique=True)
    factura = models.CharField("Factura", max_length=50, blank=True, null=True)
    tipo_doc = models.CharField("Tipo Doc", max_length=20)
    
    # Información de Cliente y Activo
    cliente = models.CharField("Cliente", max_length=255)
    unidad = models.CharField("Unidad / Placa", max_length=50)
    marca = models.CharField("Marca", max_length=50)
    
    # Gestión de Tiempos
    fecha_documento = models.DateField("Fecha Doc")
    fecha_entrega = models.DateField("Fecha Entrega", null=True, blank=True)
    
    # Valores Económicos
    venta_neta = models.DecimalField(max_digits=15, decimal_places=2)
    gross_margin = models.DecimalField(max_digits=15, decimal_places=2)
    margen_porcentaje = models.FloatField("Margen %")
    
    # Desglose de Costos (Basado en tu Excel)
    repuestos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    mano_obra = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    terceros = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.pedido} - {self.cliente}"