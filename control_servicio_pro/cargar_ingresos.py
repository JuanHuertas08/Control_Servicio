import os
import django
import pandas as pd

# 1. Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 
django.setup()

from api.models import Pedido 

def importar_datos():
    file_path = 'Base de datos.xlsx' 
    
    if not os.path.exists(file_path):
        print(f"Error: No se encontró el archivo {file_path}")
        return

    try:
        # Cargamos el Excel
        df = pd.read_excel(file_path)
        
        # Limpiamos nombres de columnas para evitar errores por espacios invisibles
        df.columns = df.columns.str.strip()

        for index, row in df.iterrows():
            # get_or_create evita duplicados si corres el script varias veces
            pedido, created = Pedido.objects.update_or_create(
                # Según el error de Django, el campo se llama 'orden_servicio' (sin el _de_)
                orden_servicio=str(row['ORDEN DE SERVICIO']), 
                defaults={
                    'cliente': row['CLIENTE'],
                    'estado': row['ESTADO'],
                    # MAPEO CRÍTICO: Aquí guardamos al asesor del Excel
                    'asesor_pssr_asignado': row['ASESOR ASIGNADO'],
                    # 'ultima_fecha_facturacion': row['FECHA'], # Descomenta si usas fechas
                }
            )
            
            accion = "Creado" if created else "Actualizado"
            print(f"{accion}: OS {row['ORDEN DE SERVICIO']} - Asesor: {row['ASESOR ASIGNADO']}")
            
        print("\n--- ¡Carga finalizada con éxito para Derco! ---")

    except Exception as e:
        print(f"Error durante la carga: {e}")

if __name__ == "__main__":
    importar_datos()