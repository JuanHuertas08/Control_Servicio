from django.urls import path
from .views import ClientePorNitView, ClienteListCreateView, RegistroServicioListCreateView

urlpatterns = [
    path("clientes/", ClienteListCreateView.as_view(), name="clientes"),
    path("clientes/<str:nit>/", ClientePorNitView.as_view(), name="cliente-por-nit"),
    path("ordenes/", RegistroServicioListCreateView.as_view(), name="ordenes-servicio"),
]
