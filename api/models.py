from django.db import models
from datetime import date

class Seguimiento(models.Model):
    # Usamos los nombres exactos de tu tabla SQLite
    Id = models.AutoField(primary_key=True, db_column='Id')
    Cliente = models.TextField(db_column='Cliente')
    Factura = models.TextField(db_column='Factura')
    Tipo_Facturacion = models.TextField(db_column='Tipo_Facturacion')
    PSSR = models.TextField(db_column='PSSR')
    Fecha_Facturacion = models.DateField(db_column='Fecha_Facturacion', null=True, blank=True)
    ESTADO = models.TextField(db_column='ESTADO')
    Fecha_Seguimiento = models.DateField(db_column='Fecha_Seguimiento', null=True, blank=True)
    Tipo_Contacto = models.TextField(db_column='Tipo_Contacto', null=True, blank=True)
    Observaciones = models.TextField(db_column='Observaciones', null=True, blank=True)

    class Meta:
        managed = True  
        db_table = 'Seguimiento'

    def __str__(self):
        return f"{self.Factura} - {self.Cliente}"
    
    @property
    def dias_transcurridos(self):
        if self.Fecha_Facturacion:
            delta = date.today() - self.Fecha_Facturacion
            return max(0, delta.days)
        return 0