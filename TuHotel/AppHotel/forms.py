from django import forms


class RegistroCliente(forms.Form):

    nombre = forms.CharField()
    documento = forms.IntegerField()
    email = forms.EmailField()


