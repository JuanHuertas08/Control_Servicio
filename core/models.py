from django.db import models


class Cliente(models.Model):
    """Maestro de clientes. Fuente única de verdad para autocompletar
    los datos del cliente al crear o cargar una orden de servicio."""

    nit = models.CharField("NIT", max_length=20, primary_key=True)
    razon_social = models.CharField("Razón Social / Nombre", max_length=255)
    telefono = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    email = models.EmailField("Correo", blank=True, null=True)
    direccion = models.CharField("Dirección", max_length=255, blank=True, null=True)
    ciudad = models.CharField("Ciudad", max_length=100, blank=True, null=True)
    contacto = models.CharField("Persona de Contacto", max_length=150, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["razon_social"]

    def __str__(self):
        return f"{self.nit} - {self.razon_social}"


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
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="ordenes_servicio",
        verbose_name="Cliente (NIT)",
    )
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
        return f"{self.pedido} - {self.cliente_id}"
