from django.urls import path
from AppHotel.views import *

urlpatterns = [
    path('', inicio, name='Inicio'),
    path('registo-cliente/', registro_cliente, name = 'RegistroClientes'),
    path('busca-cliente/', busca_clientes, name = 'BuscaCliente'),
    path('cliente-buscado/', cliente_buscado, name = 'ClienteBuscado'),
    path('registro-reserva/', registro_reserva, name = 'RegistroReservas'),
    path('ver-reservas/', ver_reservas, name = 'VerReservas'),
    path('elimina-cliente/<int:id>', eliminar_cliente, name = 'EliminaCliente'),
    path('lista-cliente/', lista_clientes, name = 'ListaClientes'),
    path('editar-cliente/<int:id>', editar_cliente, name = 'EditarClientes'),
    path('lista-habitaciones/', HabitacionList.as_view(), name = 'ListaHabitacion'),
    path('detalle-habitacion/<pk>', HabitacionDetalle.as_view(), name = 'DetalleHabitacion'),
    path('crear-habitacion/', HabitacionCrear.as_view(), name = 'CrearHabitacion'),
    path('editar-habitacion/<pk>', HabitacionEditar.as_view(), name = 'EditarHabitacion'),
    path('eliminar-habitacion/<pk>', HabitacionEliminar.as_view(), name = 'EliminarHabitacion'),

]