from django.shortcuts import render
from .models import Cliente, Habitacion, Empleado
from django.http import HttpResponse
from AppHotel.forms import RegistroCliente
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout


def inicio(self):

    return render(self, 'inicio.html')



def registro_cliente(request):
    
    if request.method == 'POST':

        miFormulario = RegistroCliente(request.POST)

        print(miFormulario)

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
    



def busca_clientes(request):

       
    return render(request, 'busca_clientes.html')


def cliente_buscado(self):

    if self.GET['nombre']:

        nombre_consulta = self.GET['nombre']
        cliente = Cliente.objects.filter(nombre=nombre_consulta).first()

        return render(self, 'cliente_buscado.html', {"cliente":cliente})

    else: 
        mensaje = f'No se Ingresaron datos'

        return render(self, 'cliente_buscado.html', {"mensaje":mensaje})



def registro_reserva(self):

    return render(self, 'registro_reserva.html')


def ver_reservas(self):

    return render(self, 'ver_reservas.html')



def eliminar_cliente(self, id):

    if self.method == 'POST':

        cliente = Cliente.objects.get(id=id)
        cliente.delete()

        mensaje = f'Cliente eliminado con éxito'

        lista_clientes = Cliente.objects.all()

        return render(self, 'lista_clientes.html', {"mensaje":mensaje , "lista_clientes":lista_clientes})



def lista_clientes(request):

    lista_clientes = Cliente.objects.all()
       
    return render(request, 'lista_clientes.html', {"lista_clientes":lista_clientes})



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
    


class HabitacionList(ListView):

    model = Habitacion
    template_name = 'lista_habitacion.html'
    context_object_name = 'habitaciones'


class HabitacionDetalle(DetailView):
    model = Habitacion
    template_name = 'detalle_habitacion.html'
    context_object_name = 'numero_habitacion'


class HabitacionCrear(CreateView):
    model = Habitacion
    template_name = 'crear_habitacion.html'
    #fields = ['numero', 'tipo', 'disponible']
    fields = '__all__'
    success_url = '/apphotel/lista-habitaciones/'


class HabitacionEditar(UpdateView):
    model = Habitacion
    template_name = 'editar_habitacion.html'
    fields = '__all__'
    success_url = '/apphotel/lista-habitaciones/'
    


class HabitacionEliminar(DeleteView):
    model = Habitacion
    template_name = 'eliminar_habitacion.html'
    success_url = '/apphotel/lista-habitaciones/'



def login(request):

    if request.method == 'POST':

        miFormulario = AuthenticationForm(request, data=request.POST)

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            usuario = data['username']
            contrasena = data['password']

            user = authenticate(username=usuario, password=contrasena)

            if user:
                login(request, user)

                return render(request, 'inicio.html', {'mensaje': f'Bienvenido {usuario}'})

        else:
            return render(request, 'inicio.html', {'mensaje' : f'Datos incorrectos'})
    
    else:
        miFormulario = RegistroCliente()
        return render(request,'registro_cliente.html', {'miFormulario': miFormulario})