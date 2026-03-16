import pandas as pd
import os
import django
from datetime import datetime

# 1. Configuración de Django (Asegúrate de que este nombre coincida con tu carpeta de proyecto)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_servicio_pro.settings')
django.setup()

# 2. Importamos el modelo correcto
from api.models import Pedido 

def limpiar_fecha(fecha):
    if pd.isna(fecha) or str(fecha).strip() == '*' or str(fecha).strip() == '':
        return None
    try:
        # Maneja tanto objetos datetime como strings de fecha
        return pd.to_datetime(fecha).date()
    except:
        return None

def limpiar_numero(valor):
    if pd.isna(valor):
        return 0
    try:
        # Quitamos comas y espacios para convertir a float
        return float(str(valor).replace(',', '').strip())
    except:
        return 0

def ejecutar_carga():
    # El nombre de tu archivo CSV
    file_path = 'Base de datos.xlsx'
    
    if not os.path.exists(file_path):
        print(f"Error: No se encontró el archivo {file_path}")
        return

    # Cargamos el CSV. Si el separador es diferente a la coma, cámbialo aquí
    df = pd.read_excel('Base de datos.xlsx')
    
    print(f"Iniciando carga de {len(df)} registros en la base de datos...")

    for index, row in df.iterrows():
        try:
            # Mapeo de las columnas del CSV a los campos del modelo Pedido
            Pedido.objects.update_or_create(
                orden_servicio=str(row['Pedido']), # Usamos 'Pedido' como identificador único
                defaults={
                    'cliente': row['CLIENTE'],
                    'ultima_fecha_facturacion': limpiar_fecha(row['Fecha documento']),
                    'tipo_facturacion': row['Tipo Doc'] if 'Tipo Doc' in row else 'ESTIBADORES',
                    'ultimo_asesor_facturo': row['PSSR'] if 'PSSR' in row else 'N/A',
                    'asesor_pssr_asignado': row['PSSR'] if 'PSSR' in row else 'N/A',
                    'estado': 'ACTIVO'
                }
            )
            
            if index % 50 == 0:
                print(f"Procesados {index} registros...")

        except Exception as e:
            print(f"Error en fila {index} (Pedido {row.get('Pedido')}): {e}")

    print("¡Carga masiva finalizada con éxito!")

if __name__ == "__main__":
    ejecutar_carga()