import pandas as pd
import os
import django

# 1. Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_servicio_pro.settings')
django.setup()

# 2. Modelos: el maestro de clientes y las órdenes de servicio
from core.models import Cliente, RegistroServicio


def limpiar_fecha(fecha):
    if pd.isna(fecha) or str(fecha).strip() in ('', '*'):
        return None
    try:
        return pd.to_datetime(fecha).date()
    except Exception:
        return None


def limpiar_numero(valor):
    if pd.isna(valor):
        return 0
    try:
        return float(str(valor).replace(',', '').replace('$', '').strip())
    except Exception:
        return 0


def limpiar_texto(valor):
    if valor is None or pd.isna(valor):
        return None
    texto = str(valor).strip()
    return texto or None


def ejecutar_carga():
    file_path = 'Base de datos.xlsx'

    if not os.path.exists(file_path):
        print(f"Error: No se encontró el archivo {file_path}")
        return

    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()

    if 'NIT' not in df.columns:
        print(
            "Error: la plantilla no tiene columna 'NIT'. Agrega la columna NIT "
            "(identificación del cliente) antes de cargar el archivo: es obligatoria "
            "para construir y mantener el maestro de clientes."
        )
        return

    print(f"Iniciando carga de {len(df)} registros...")

    clientes_creados = clientes_actualizados = 0
    ordenes_ok = filas_omitidas = 0

    for index, row in df.iterrows():
        nit = limpiar_texto(row.get('NIT'))
        pedido = row.get('Pedido')

        if not nit:
            filas_omitidas += 1
            print(f"Fila {index + 2} (Pedido {pedido}): omitida, no tiene NIT.")
            continue

        # 1. Aseguramos el maestro de clientes con la información disponible en la fila
        cliente, creado = Cliente.objects.update_or_create(
            nit=nit,
            defaults={
                'razon_social': limpiar_texto(row.get('CLIENTE')) or nit,
                'telefono': limpiar_texto(row.get('Telefono') or row.get('Teléfono')),
                'email': limpiar_texto(row.get('Email') or row.get('Correo')),
                'direccion': limpiar_texto(row.get('Direccion') or row.get('Dirección')),
                'ciudad': limpiar_texto(row.get('Ciudad')),
            },
        )
        clientes_creados += int(creado)
        clientes_actualizados += int(not creado)

        # 2. Registramos/actualizamos la orden de servicio, ya vinculada al cliente
        try:
            RegistroServicio.objects.update_or_create(
                pedido=int(pedido),
                defaults={
                    'centro': limpiar_texto(row.get('Centro')) or '',
                    'centro_beneficio': limpiar_texto(row.get('Centro de Beneficio')) or '',
                    'pssr': limpiar_texto(row.get('PSSR')) or '',
                    'factura': limpiar_texto(row.get('FACTURA')),
                    'tipo_doc': limpiar_texto(row.get('Tipo Doc')) or '',
                    'cliente': cliente,
                    'unidad': limpiar_texto(row.get('Unidad')) or '',
                    'marca': limpiar_texto(row.get('Marca')) or '',
                    'fecha_documento': limpiar_fecha(row.get('Fecha documento')),
                    'fecha_entrega': limpiar_fecha(row.get('Fecha de facturación')),
                    'venta_neta': limpiar_numero(row.get('Venta Neta')),
                    'gross_margin': limpiar_numero(row.get('Gross Margin $')),
                    'margen_porcentaje': limpiar_numero(row.get('Margen %')),
                    'repuestos': limpiar_numero(row.get('repuestos')),
                    'mano_obra': limpiar_numero(row.get('Mano de obra')),
                    'terceros': limpiar_numero(row.get('Trabajos de Terceros')),
                },
            )
            ordenes_ok += 1
        except Exception as e:
            print(f"Fila {index + 2} (Pedido {pedido}): error al guardar la orden -> {e}")

    print(
        "Carga finalizada. "
        f"Clientes nuevos: {clientes_creados}, clientes actualizados: {clientes_actualizados}, "
        f"órdenes cargadas: {ordenes_ok}, filas omitidas por falta de NIT: {filas_omitidas}"
    )


if __name__ == "__main__":
    ejecutar_carga()
