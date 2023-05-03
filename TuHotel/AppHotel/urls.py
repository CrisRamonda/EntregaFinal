from django.urls import path
from AppHotel.views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', inicio, name='Inicio'),
    path('registo-cliente/', registro_cliente, name = 'RegistroClientes'),
    path('busca-cliente/', busca_clientes, name = 'BuscaCliente'),
    path('cliente-buscado/', cliente_buscado, name = 'ClienteBuscado'),
    path('registro-reserva/', registro_reserva, name = 'RegistroReservas'),
    path('buscar-reservas/', buscar_reservas, name = 'BuscarReservas'),
    path('elimina-cliente/<int:id>', eliminar_cliente, name = 'EliminaCliente'),
    path('lista-cliente/', lista_clientes, name = 'ListaClientes'),
    path('editar-cliente/<int:id>', editar_cliente, name = 'EditarClientes'),
    path('lista-habitaciones/', HabitacionList.as_view(), name = 'ListaHabitacion'),
    path('detalle-habitacion/<pk>', HabitacionDetalle.as_view(), name = 'DetalleHabitacion'),
    path('crear-habitacion/', HabitacionCrear.as_view(), name = 'CrearHabitacion'),
    path('editar-habitacion/<pk>', HabitacionEditar.as_view(), name = 'EditarHabitacion'),
    path('eliminar-habitacion/<pk>', HabitacionEliminar.as_view(), name = 'EliminarHabitacion'),
    path('login/', login_usuario, name = 'Login'),
    path('registrar/', registrar_usuario, name = 'Registrar'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name = 'Logout'),
    path('editar-usuario/', editar_usuario, name = 'EditarUsuario'),
    path('lista-reservas/', lista_reservas, name = 'ListaReservas'),

]
