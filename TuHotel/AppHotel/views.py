from AppHotel.forms import RegistroCliente, UserEditForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,UpdateView)
from .models import Avatar, Cliente, Empleado, Habitacion


#VISTAS GENERALES
def inicio(self):
    try: 
        avatar = Avatar.objects.get(user=self.user.id)
        return render(self, 'inicio.html', {'url': avatar.imagen.url })
    except:
        return render(self, 'inicio.html')
       
def about(self):
    try: 
        avatar = Avatar.objects.get(user=self.user.id)
        return render(self, 'about.html', {'url': avatar.imagen.url })
    except:
        return render(self, 'about.html')


def en_construccion(self):
    try: 
        avatar = Avatar.objects.get(user=self.user.id)
        return render(self, 'en_construccion.html', {'url': avatar.imagen.url })
    except:
        return render(self, 'en_construccion.html')


#VISTAS DE LOGIN REGISTRO
def login_usuario(request):

    if request.method == 'POST':

        miFormulario = AuthenticationForm(request, data=request.POST)
        
        #para agregarle labels a los campos de un formulario 
        miFormulario.fields['username'].label = 'Usuario'
        miFormulario.fields['password'].label = 'Contraseña'

        #modificar atributo widget del objeto para agregar la clase de bootstrap
        miFormulario.fields['username'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['password'].widget.attrs.update({'class': 'form-control'})

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            usuario = data['username']
            contrasena = data['password']

            user = authenticate(username=usuario, password=contrasena)

            if user:
                login(request, user)

                try: 
                    avatar = Avatar.objects.get(user=request.user.id)
                    return render(request, 'login.html', {'mensaje': f'¡Bienvenido {usuario}!',  'miFormulario': miFormulario ,'url': avatar.imagen.url })
                except:
                    return render(request, 'login.html', {'mensaje': f'¡Bienvenido {usuario}!',  'miFormulario': miFormulario})

                

        else:
            return render(request, 'login.html', {'mensaje' : f'Datos de ingreso incorrectos','mensaje2': f'Intente nuevamente' , 'miFormulario': miFormulario})
    
    else:
        miFormulario = AuthenticationForm()
        miFormulario.fields['username'].label = 'Usuario'
        miFormulario.fields['password'].label = 'Contraseña'

        miFormulario.fields['username'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['password'].widget.attrs.update({'class': 'form-control'})

        return render(request,'login.html', {'miFormulario': miFormulario})
    

def registrar_usuario(request):
    
    if request.method == 'POST':

        miFormulario = UserCreationForm(request.POST)
        miFormulario.fields['username'].label = 'Usuario'
        miFormulario.fields['password1'].label = 'Contraseña'
        miFormulario.fields['password2'].label = 'Repetir Contraseña'

        miFormulario.fields['username'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['password1'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['password2'].widget.attrs.update({'class': 'form-control'})

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
            usuario = data['username']
            #contrasena = data['password']
            miFormulario.save()
            return render(request, 'registro.html', {'mensaje1': f'¡Usuario {usuario} creado!', 'miFormulario': miFormulario})

        else:
            
            return render(request, 'registro.html', {'mensaje2' : f'¡Datos de registro incorrectos! Intente nuevamente', 'miFormulario': miFormulario})
    
    else:
        miFormulario = UserCreationForm()
        miFormulario.fields['username'].label = 'Usuario'
        miFormulario.fields['password1'].label = 'Contraseña'
        miFormulario.fields['password2'].label = 'Repetir Contraseña'

        miFormulario.fields['username'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['password1'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['password2'].widget.attrs.update({'class': 'form-control'})

        return render(request,'registro.html', {'miFormulario': miFormulario})
    

@login_required
def editar_usuario(request):

    usuario = request.user

    if request.method == 'POST':

        miFormulario = UserEditForm(request.POST, instance=request.user)
        miFormulario.fields['first_name'].label = 'Nombre'
        miFormulario.fields['last_name'].label = 'Apellido'
        miFormulario.fields['email'].label = 'E-Mail'


        miFormulario.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['last_name'].widget.attrs.update({'class': 'form-control'})        
        miFormulario.fields['email'].widget.attrs.update({'class': 'form-control'})        
        miFormulario.fields['password1'].widget.attrs.update({'class': 'form-control'})        
        miFormulario.fields['password2'].widget.attrs.update({'class': 'form-control'})        

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
        
            usuario.first_name = data['first_name']
            usuario.last_name = data['last_name']
            usuario.email = data['email']

            usuario.set_password(data['password1'])
            usuario.save()

            try: 
                avatar = Avatar.objects.get(user=request.user.id)
                return render(request, 'editar_usuario.html', {'edicion_exitosa': 'Edición realizada con éxito','url': avatar.imagen.url })
            except:
                return render(request, 'editar_usuario.html', {'edicion_exitosa': 'Edición realizada con éxito' })

            

        else:

            try: 
                avatar = Avatar.objects.get(user=request.user.id)
                return render(request, 'editar_usuario.html', {'edicion_fallida': 'Datos del formulario inválidos', 'miFormulario': miFormulario,'url': avatar.imagen.url })
            except:
                return render(request, 'editar_usuario.html', {'edicion_fallida': 'Datos del formulario inválidos', 'miFormulario': miFormulario})
            
     
    else:
        miFormulario = UserEditForm(instance=request.user)
        miFormulario.fields['first_name'].label = 'Nombre'
        miFormulario.fields['last_name'].label = 'Apellido'
        miFormulario.fields['email'].label = 'E-Mail'

        miFormulario.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['last_name'].widget.attrs.update({'class': 'form-control'})        
        miFormulario.fields['email'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['password1'].widget.attrs.update({'class': 'form-control'})        
        miFormulario.fields['password2'].widget.attrs.update({'class': 'form-control'})

        try: 
            avatar = Avatar.objects.get(user=request.user.id)
            return render(request, 'editar_usuario.html', {'miFormulario': miFormulario,'url': avatar.imagen.url })
        except:
            return render(request,'editar_usuario.html', {'miFormulario': miFormulario})



#VISTAS DE CLIENTES      
@login_required
def registro_cliente(request):
    
    if request.method == 'POST':

        miFormulario = RegistroCliente(request.POST)
        miFormulario.fields['nombre'].label = 'Nombre'
        miFormulario.fields['documento'].label = 'Documento'
        miFormulario.fields['email'].label = 'E-Mail'

        miFormulario.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['documento'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['email'].widget.attrs.update({'class': 'form-control'})

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data

            cliente = Cliente(
                nombre = data['nombre'],
                documento = data['documento'],
                email = data['email']
            )
            cliente.save()


            try: 
                avatar = Avatar.objects.get(user=request.user.id)
                return render(request, 'registro_cliente.html', {'registro_exitoso': 'Registro realizado con éxito' , 'url': avatar.imagen.url })
            except:
                return render(request, 'registro_cliente.html', {'registro_exitoso': 'Registro realizado con éxito'} ) 

                       


        else:  
            try: 
                avatar = Avatar.objects.get(user=request.user.id)
                return render(request, 'registro_cliente.html', {'registro_fallido': 'Datos del formulario inválidos' , 'url': avatar.imagen.url })
            except:
                return render(request, 'registro_cliente.html', {'registro_fallido': 'Datos del formulario inválidos'} ) 


    
    else:
        
        miFormulario = RegistroCliente()

        miFormulario.fields['nombre'].label = 'Nombre'
        miFormulario.fields['documento'].label = 'Documento'
        miFormulario.fields['email'].label = 'E-Mail'

        miFormulario.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['documento'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['email'].widget.attrs.update({'class': 'form-control'})

        try: 
            avatar = Avatar.objects.get(user=request.user.id)
            return render(request, 'registro_cliente.html', {'miFormulario': miFormulario , 'url': avatar.imagen.url })
        except:
            return render(request, 'registro_cliente.html', {'miFormulario': miFormulario} )     


@login_required
def busca_clientes(request):
    try: 
        avatar = Avatar.objects.get(user=request.user.id)
        return render(request, 'busca_clientes.html', {'url': avatar.imagen.url })
    except:
        return render(request, 'busca_clientes.html')


@login_required
def cliente_buscado(self):

    if self.GET['nombre']:

        nombre_consulta = self.GET['nombre']
        cliente = Cliente.objects.filter(nombre=nombre_consulta).first()

        try: 
            avatar = Avatar.objects.get(user=self.user.id)
            return render(self, 'cliente_buscado.html', {"cliente":cliente , 'url': avatar.imagen.url })
        except:
            return render(self, 'cliente_buscado.html', {"cliente":cliente})


    else: 
        mensaje = f'No se Ingresaron datos'

        try: 
            avatar = Avatar.objects.get(user=self.user.id)
            return render(self, 'cliente_buscado.html', {"mensaje":mensaje , 'url': avatar.imagen.url })
        except:
            return render(self, 'cliente_buscado.html', {"mensaje":mensaje})


@login_required
def eliminar_cliente(self, id):

    if self.method == 'POST':

        cliente = Cliente.objects.get(id=id)
        cliente.delete()

        mensaje = f'Cliente eliminado con éxito'

        lista_clientes = Cliente.objects.all()

        try: 
            avatar = Avatar.objects.get(user=self.user.id)
            return render(self, 'lista_clientes.html', {"mensaje":mensaje , "lista_clientes":lista_clientes , 'url': avatar.imagen.url })
        except:
            return render(self, 'lista_clientes.html', {"mensaje":mensaje , "lista_clientes":lista_clientes})


@login_required
def lista_clientes(request):

    lista_clientes = Cliente.objects.all()

    try: 
        avatar = Avatar.objects.get(user=request.user.id)
        return render(request, 'lista_clientes.html', {"lista_clientes":lista_clientes , 'url': avatar.imagen.url })
    except:
        return render(request, 'lista_clientes.html', {"lista_clientes":lista_clientes})


@login_required
def editar_cliente(request, id):
    
    cliente = Cliente.objects.get(id=id)

    if request.method == 'POST':

        miFormulario = RegistroCliente(request.POST)
        miFormulario.fields['nombre'].label = 'Nombre'
        miFormulario.fields['documento'].label = 'Documento'
        miFormulario.fields['email'].label = 'E-Mail'

        miFormulario.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['documento'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['email'].widget.attrs.update({'class': 'form-control'})

        if miFormulario.is_valid():

            data = miFormulario.cleaned_data
        
            cliente.nombre = data['nombre']
            cliente.documento = data['documento']
            cliente.email = data['email']
            cliente.save()

            lista_clientes = Cliente.objects.all()

            try: 
                avatar = Avatar.objects.get(user=request.user.id)
                return render(request, 'lista_clientes.html', {'edicion_exitosa': '¡Edición realizada con éxito!' , "lista_clientes":lista_clientes , 'url': avatar.imagen.url })
            except:
                return render(request, 'lista_clientes.html', {'edicion_exitosa': '¡Edición realizada con éxito!' , "lista_clientes":lista_clientes})


        else:
            
            lista_clientes = Cliente.objects.all()

            try: 
                avatar = Avatar.objects.get(user=request.user.id)
                return render(request, 'lista_clientes.html', {'edicion_fallida': 'Datos del formulario inválidos' , "lista_clientes":lista_clientes , 'url': avatar.imagen.url })
            except:
                return render(request, 'lista_clientes.html', {'edicion_fallida': 'Datos del formulario inválidos' , "lista_clientes":lista_clientes})

     
    else:
        
        miFormulario = RegistroCliente(initial={
            'nombre' : cliente.nombre,
            'documento' : cliente.documento,
            'email' : cliente.email
            
        })

        miFormulario.fields['nombre'].label = 'Nombre'
        miFormulario.fields['documento'].label = 'Documento'
        miFormulario.fields['email'].label = 'E-Mail'

        miFormulario.fields['nombre'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['documento'].widget.attrs.update({'class': 'form-control'})
        miFormulario.fields['email'].widget.attrs.update({'class': 'form-control'})

        try: 
            avatar = Avatar.objects.get(user=request.user.id)
            return render(request, 'editar_cliente.html', {'miFormulario': miFormulario, 'id' : cliente.id , 'url': avatar.imagen.url })
        except:
            return render(request,'editar_cliente.html', {'miFormulario': miFormulario, 'id' : cliente.id})


#VISTA EMPLEADO
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


#VISTAS DE RESERVAS
def lista_reservas(self):
    try: 
        avatar = Avatar.objects.get(user=self.user.id)
        return render(self, 'lista_reservas.html', {'url': avatar.imagen.url })
    except:
        return render(self, 'lista_reservas.html')


def registro_reserva(self):
    try: 
        avatar = Avatar.objects.get(user=self.user.id)
        return render(self, 'registro_reserva.html', {'url': avatar.imagen.url })
    except:
        return render(self, 'registro_reserva.html')


def buscar_reservas(self):
    try: 
        avatar = Avatar.objects.get(user=self.user.id)
        return render(self, 'buscar_reservas.html', {'url': avatar.imagen.url })
    except:
        return render(self, 'buscar_reservas.html')


#VISTAS DE HABITACIONES  (Basadas en clases)
class HabitacionList(LoginRequiredMixin, ListView):

    model = Habitacion
    template_name = 'lista_habitacion.html'
    context_object_name = 'habitaciones'

    #funcion para pasarle un contexto, en este caso el try-except del avatar
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            avatar = Avatar.objects.get(user=self.request.user.id)
            context['url'] = avatar.imagen.url
        except Avatar.DoesNotExist:
            pass
        return context


class HabitacionDetalle(LoginRequiredMixin, DetailView):
    model = Habitacion
    template_name = 'detalle_habitacion.html'
    context_object_name = 'numero_habitacion'

    #funcion para agregarle la clase de bootstrap al formulario
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['numero'].widget.attrs.update({'class': 'form-control'})
        form.fields['tipo'].widget.attrs.update({'class': 'form-control'})
        form.fields['disponible'].widget.attrs.update({'class': 'form-check-input'})
        return form
    
    #funcion para pasarle un contexto, en este caso el try-except del avatar
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            avatar = Avatar.objects.get(user=self.request.user.id)
            context['url'] = avatar.imagen.url
        except Avatar.DoesNotExist:
            pass
        return context


class HabitacionCrear(LoginRequiredMixin, CreateView):
    model = Habitacion
    template_name = 'crear_habitacion.html'
    #fields = ['numero', 'tipo', 'disponible']
    fields = '__all__'
    success_url = '/apphotel/lista-habitaciones/'


    #funcion para agregarle la clase de bootstrap al formulario
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['numero'].widget.attrs.update({'class': 'form-control'})
        form.fields['tipo'].widget.attrs.update({'class': 'form-control'})
        form.fields['disponible'].widget.attrs.update({'class': 'form-check-input'})
        return form
    
    #funcion para pasarle un contexto, en este caso el try-except del avatar
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            avatar = Avatar.objects.get(user=self.request.user.id)
            context['url'] = avatar.imagen.url
        except Avatar.DoesNotExist:
            pass
        return context


class HabitacionEditar(LoginRequiredMixin, UpdateView):
    model = Habitacion
    template_name = 'editar_habitacion.html'
    fields = '__all__'
    success_url = '/apphotel/lista-habitaciones/'

    #funcion para agregarle la clase de bootstrap al formulario
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['numero'].widget.attrs.update({'class': 'form-control'})
        form.fields['tipo'].widget.attrs.update({'class': 'form-control'})
        form.fields['disponible'].widget.attrs.update({'class': 'form-check-input'})
        return form
    
    #funcion para pasarle un contexto, en este caso el try-except del avatar
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            avatar = Avatar.objects.get(user=self.request.user.id)
            context['url'] = avatar.imagen.url
        except Avatar.DoesNotExist:
            pass
        return context
    

class HabitacionEliminar(DeleteView):
    model = Habitacion
    template_name = 'eliminar_habitacion.html'
    success_url = '/apphotel/lista-habitaciones/'

    #funcion para pasarle un contexto, en este caso el try-except del avatar
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            avatar = Avatar.objects.get(user=self.request.user.id)
            context['url'] = avatar.imagen.url
        except Avatar.DoesNotExist:
            pass
        return context




    


