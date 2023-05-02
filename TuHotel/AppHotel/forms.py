from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import Empleado
from django.contrib.auth.models import User


class RegistroCliente(forms.Form):

    nombre = forms.CharField()
    documento = forms.IntegerField()
    email = forms.EmailField()


# class RegistrarEmpleado(forms.ModelForm):

#     class Meta:
#         model = Empleado
#         fields = '__all__'


class UserEditForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = {'first_name','last_name' , 'email', 'password1', 'password2'}


    #agregamos campos que no son del modelo en sí
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir Contraseña', widget=forms.PasswordInput)

    def clean_password1(self):

        password2 = self.cleaned_data['password2']
        
        if password2 != self.cleaned_data['password1']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2