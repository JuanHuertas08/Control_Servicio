from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Seguimiento  # Asegúrate de que el modelo se llame Seguimiento
from .serializers import SeguimientoSerializer # Necesitarás crear este serializer

# --- 1. CONFIGURACIÓN DE PAGINACIÓN ---
class EstandarPaginacion(PageNumberPagination):
    page_size = 15 
    page_size_query_param = 'page_size'
    max_page_size = 100

# --- 2. VISTA PARA FILTROS DINÁMICOS (Opciones únicas) ---
@api_view(['GET'])
def opciones_filtros(request):
    """
    Retorna listas únicas para llenar los selectores del frontend
    """
    try:
        # Extraer valores únicos directamente de la BD
        clientes = Seguimiento.objects.values_list('Cliente', flat=True).distinct().order_by('Cliente')
        asesores = Seguimiento.objects.values_list('PSSR', flat=True).distinct().order_by('PSSR')
        tipos = Seguimiento.objects.values_list('Tipo_Facturacion', flat=True).distinct().order_by('Tipo_Facturacion')

        return Response({
            "clientes": list(filter(None, clientes)),
            "asesores": list(filter(None, asesores)),
            "tipos_facturacion": list(filter(None, tipos))
        })
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- 3. VISTA PRINCIPAL DE SEGUIMIENTOS ---
class SeguimientosView(APIView):
    def get(self, request):
        try:
            # Iniciamos el queryset con la nueva tabla
            queryset = Seguimiento.objects.all().order_by('-Id')
            
            # Capturamos parámetros de Angular (deben coincidir con el data.service.ts)
            cliente = request.query_params.get('cliente', None)
            pssr = request.query_params.get('pssr', None) 
            tipo = request.query_params.get('tipo_facturacion', None)

            # Filtros aplicados usando los nuevos nombres de campos (Case Sensitive)
            if cliente:
                queryset = queryset.filter(Cliente__icontains=cliente)
            
            if pssr:
                queryset = queryset.filter(PSSR=pssr)
            
            if tipo:
                queryset = queryset.filter(Tipo_Facturacion=tipo)

            # Paginación
            paginador = EstandarPaginacion()
            resultado_paginado = paginador.paginate_queryset(queryset, request, view=self)
            
            if resultado_paginado is not None:
                serializer = SeguimientoSerializer(resultado_paginado, many=True)
                return paginador.get_paginated_response(serializer.data)

            serializer = SeguimientoSerializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            print(f"Error en SeguimientosView: {e}") 
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Para registrar el contacto realizado (Botón Seguimiento)
        """
        try:
            id_registro = request.data.get('id')
            seguimiento = Seguimiento.objects.get(Id=id_registro)
            seguimiento.Tipo_Contacto = request.data.get('tipo_contacto')
            seguimiento.Fecha_Seguimiento = request.data.get('fecha_seguimiento')
            seguimiento.Observaciones = request.data.get('observaciones')
            seguimiento.ESTADO = 'REALIZADO'
            
            seguimiento.save()
            return Response({"message": "Seguimiento actualizado correctamente"}, status=status.HTTP_200_OK)
        except Seguimiento.DoesNotExist:
            return Response({"error": "Registro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # En api/views.py dentro de la clase SeguimientosView o en una función dedicada
def post(self, request):
    try:
        id_registro = request.data.get('id')
        # Buscamos el registro por su ID
        seguimiento = Seguimiento.objects.get(Id=id_registro)
        
        # Actualizamos con la información enviada desde Angular
        seguimiento.Tipo_Contacto = request.data.get('tipo_contacto')
        seguimiento.Fecha_Seguimiento = request.data.get('fecha_seguimiento')
        seguimiento.Observaciones = request.data.get('observaciones')
        seguimiento.ESTADO = '0' 
        
        seguimiento.save()
        return Response({"message": "Seguimiento guardado y estado actualizado a REALIZADO"}, status=status.HTTP_200_OK)
    
    except Seguimiento.DoesNotExist:
        return Response({"error": "Registro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)