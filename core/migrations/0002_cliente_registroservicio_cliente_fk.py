from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('nit', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='NIT')),
                ('razon_social', models.CharField(max_length=255, verbose_name='Razón Social / Nombre')),
                ('telefono', models.CharField(blank=True, max_length=50, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Dirección')),
                ('ciudad', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ciudad')),
                ('contacto', models.CharField(blank=True, max_length=150, null=True, verbose_name='Persona de Contacto')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['razon_social'],
            },
        ),
        migrations.AlterField(
            model_name='registroservicio',
            name='cliente',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='ordenes_servicio',
                to='core.cliente',
                verbose_name='Cliente (NIT)',
            ),
        ),
    ]
