from django.urls import path
from .views import SeguimientosView, opciones_filtros

urlpatterns = [
    # Cambiamos PedidosView por SeguimientosView
    path('pedidos/', SeguimientosView.as_view(), name='pedidos'),
    path('opciones-filtros/', opciones_filtros, name='opciones-filtros'),
]
