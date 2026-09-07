from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Cliente, RegistroServicio
from .serializers import ClienteSerializer, RegistroServicioSerializer


class ClientePorNitView(APIView):
    """Autocompletado: dado un NIT, retorna los datos del cliente
    (nombre, teléfono, email, dirección, etc.) para llenar el
    formulario de orden de servicio."""

    def get(self, request, nit):
        try:
            cliente = Cliente.objects.get(nit=nit)
        except Cliente.DoesNotExist:
            return Response(
                {"error": "No existe un cliente con ese NIT en el maestro de clientes."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(ClienteSerializer(cliente).data)


class ClienteListCreateView(ListCreateAPIView):
    """Lista/búsqueda de clientes (?q=) y alta de clientes nuevos
    en el maestro cuando aún no existen."""

    serializer_class = ClienteSerializer

    def get_queryset(self):
        queryset = Cliente.objects.all()
        q = self.request.query_params.get("q")
        if q:
            queryset = queryset.filter(razon_social__icontains=q) | queryset.filter(nit__icontains=q)
        return queryset


class RegistroServicioListCreateView(ListCreateAPIView):
    """Creación de órdenes de servicio. El cliente se resuelve por NIT
    contra el maestro de clientes (Cliente)."""

    queryset = RegistroServicio.objects.select_related("cliente").order_by("-fecha_documento")
    serializer_class = RegistroServicioSerializer
