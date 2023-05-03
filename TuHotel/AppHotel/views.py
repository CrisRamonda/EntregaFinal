from django.shortcuts import render
from .models import Cliente, Habitacion, Empleado, Avatar
from django.http import HttpResponse
from AppHotel.forms import RegistroCliente, UserEditForm
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User



def inicio(self):
    try: 
        avatar = Avatar.objects.get(user=self.user.id)
        return render(self, 'inicio.html', {'url': avatar.imagen.url })
    except:
        return render(self, 'inicio.html')

       
    
  


@login_required
def registro_cliente(request):
    
    if request.method == 'POST':

        miFormulario = RegistroCliente(request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data

            cliente = Cliente(
                nombre = data['nombre'],
                documento = data['documento'],
                email = data['email']
            )
            cliente.save()
            return render(request, 'registro_cliente.html', {'registro_exitoso': 'Registro realizado con éxito'})

        else:       
            return render(request, 'registro_cliente.html', {'registro_fallido': 'Datos del formulario inválidos'})
    
    else:
        
        miFormulario = RegistroCliente()       
        return render(request,'registro_cliente.html', {'miFormulario': miFormulario})
    


@login_required
def busca_clientes(request):

       
    return render(request, 'busca_clientes.html')


@login_required
def cliente_buscado(self):

    if self.GET['nombre']:

        nombre_consulta = self.GET['nombre']
        cliente = Cliente.objects.filter(nombre=nombre_consulta).first()

        return render(self, 'cliente_buscado.html', {"cliente":cliente})

    else: 
        mensaje = f'No se Ingresaron datos'

        return render(self, 'cliente_buscado.html', {"mensaje":mensaje})



@login_required
def eliminar_cliente(self, id):

    if self.method == 'POST':

        cliente = Cliente.objects.get(id=id)
        cliente.delete()

        mensaje = f'Cliente eliminado con éxito'

        lista_clientes = Cliente.objects.all()

        return render(self, 'lista_clientes.html', {"mensaje":mensaje , "lista_clientes":lista_clientes})


@login_required
def lista_clientes(request):

    lista_clientes = Cliente.objects.all()
       
    return render(request, 'lista_clientes.html', {"lista_clientes":lista_clientes})


@login_required
def editar_cliente(request, id):
    
    cliente = Cliente.objects.get(id=id)

    if request.method == 'POST':

        miFormulario = RegistroCliente(request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
        
            cliente.nombre = data['nombre']
            cliente.documento = data['documento']
            cliente.email = data['email']
            cliente.save()

            lista_clientes = Cliente.objects.all()

            return render(request, 'lista_clientes.html', {'edicion_exitosa': 'Edición realizada con éxito' , "lista_clientes":lista_clientes})

        else:
            
            lista_clientes = Cliente.objects.all()

            return render(request, 'lista_clientes.html', {'edicion_fallida': 'Datos del formulario inválidos' , "lista_clientes":lista_clientes})
     
    else:
        
        miFormulario = RegistroCliente(initial={
            'nombre' : cliente.nombre,
            'documento' : cliente.documento,
            'email' : cliente.email
            
        })
        
        return render(request,'editar_cliente.html', {'miFormulario': miFormulario, 'id' : cliente.id})



# @staff_member_required
# def registro_empleado(request):
    
#     if request.method == 'POST':

#         miFormulario = RegistrarEmpleado(request.POST)

#         if miFormulario.is_valid():

#             data = miFormulario.cleaned_data

#             empleado = Empleado(
#                 nombre = data['nombre'],
#                 documento = data['documento'],
#                 email = data['email'],
#                 puesto = data['puesto']
#             )
#             empleado.save()
#             return render(request, 'registro_empleado.html', {'registro_exitoso': 'Registro realizado con éxito'})

#         else:       
#             return render(request, 'registro_empleado.html', {'registro_fallido': 'Datos del formulario inválidos'})
    
#     else:
        
#         miFormulario = RegistrarEmpleado()       
#         return render(request,'registro_empleado.html', {'miFormulario': miFormulario})


def lista_reservas(self):

    return render(self, 'lista_reservas.html')

def registro_reserva(self):

    return render(self, 'registro_reserva.html')


def buscar_reservas(self):

    return render(self, 'buscar_reservas.html')




class HabitacionList(LoginRequiredMixin, ListView):

    model = Habitacion
    template_name = 'lista_habitacion.html'
    context_object_name = 'habitaciones'


class HabitacionDetalle(LoginRequiredMixin, DetailView):
    model = Habitacion
    template_name = 'detalle_habitacion.html'
    context_object_name = 'numero_habitacion'


class HabitacionCrear(LoginRequiredMixin, CreateView):
    model = Habitacion
    template_name = 'crear_habitacion.html'
    #fields = ['numero', 'tipo', 'disponible']
    fields = '__all__'
    success_url = '/apphotel/lista-habitaciones/'


class HabitacionEditar(LoginRequiredMixin, UpdateView):
    model = Habitacion
    template_name = 'editar_habitacion.html'
    fields = '__all__'
    success_url = '/apphotel/lista-habitaciones/'
    


class HabitacionEliminar(DeleteView):
    model = Habitacion
    template_name = 'eliminar_habitacion.html'
    success_url = '/apphotel/lista-habitaciones/'



def login_usuario(request):

    if request.method == 'POST':

        miFormulario = AuthenticationForm(request, data=request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            usuario = data['username']
            contrasena = data['password']

            user = authenticate(username=usuario, password=contrasena)

            if user:
                login(request, user)

                return render(request, 'login.html', {'mensaje': f'Bienvenido {usuario}' , 'miFormulario': miFormulario})

        else:
            return render(request, 'login.html', {'mensaje' : f'Datos de ingreso incorrectos', 'miFormulario': miFormulario})
    
    else:
        miFormulario = AuthenticationForm()
        return render(request,'login.html', {'miFormulario': miFormulario})
    


def registrar_usuario(request):
    
    if request.method == 'POST':

        miFormulario = UserCreationForm(data=request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            usuario = data['username']
            #contrasena = data['password']
            miFormulario.save()
            return render(request, 'registro.html', {'mensaje': f'Usuario {usuario} creado!', 'miFormulario': miFormulario})


        else:
            return render(request, 'registro.html', {'mensaje' : f'¡Datos de ingreso incorrectos!', 'miFormulario': miFormulario})
    
    else:
        miFormulario = UserCreationForm()
        return render(request,'registro.html', {'miFormulario': miFormulario})
    

@login_required
def editar_usuario(request):

    usuario = request.user

    if request.method == 'POST':

        miFormulario = UserEditForm(request.POST, instance=request.user)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
        
            usuario.first_name = data['first_name']
            usuario.last_name = data['last_name']
            usuario.email = data['email']

            usuario.set_password(data['password1'])
            usuario.save()

            return render(request, 'editar_usuario.html', {'edicion_exitosa': 'Edición realizada con éxito' })

        else:
            return render(request, 'editar_usuario.html', {'edicion_fallida': 'Datos del formulario inválidos', 'miFormulario': miFormulario})
     
    else:
        miFormulario = UserEditForm(instance=request.user)
        return render(request,'editar_usuario.html', {'miFormulario': miFormulario})


    


