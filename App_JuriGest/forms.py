from django import forms
from .models import UsuarioBase, Doctrina, Sentencia
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime

class CreacionUsuarioCustom(UserCreationForm):
    class Meta:
        model = UsuarioBase
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'tipo']

    username = forms.CharField(label='Usuario:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Su usuario...'}))
    password1 = forms.CharField(label='Contraseña:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}))
    password2 = forms.CharField(label='Confirma tu contraseña:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}))
    first_name = forms.CharField(label='Nombre:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Su nombre...'}))
    last_name = forms.CharField(label='Apellido:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Su apellido...'}))
    tipo = forms.ChoiceField(label='Tipo:', choices=[('juez', 'Juez'), ('lector', 'Lector')], widget=forms.Select(attrs={'class': 'form-control'}))

class IngresoCustom(AuthenticationForm):
    class Meta: 
        model = UsuarioBase
        fields = ['username', 'password']

    username = forms.CharField(label='Usuario:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label='Contraseña:', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class FiltradoSentencias(forms.Form):
    AÑOS = [(r, r) for r in range(1980, datetime.date.today().year+1)]
    AÑOS = [('todos', 'Todos')] + AÑOS

    REVISTA_O_PROVINCIAL = [
        ('todos', 'Todos'),
        ('Revista', 'Revista'),
        ('Provincial', 'Provincial'),
    ]

    INSTANCIA_CHOICES = [
        ('todos', 'Todos'),
        ('primer instancia', 'Primer instancia'),
        ('segunda instancia', 'Segunda instancia'),
        ('tercera instancia', 'Tercera instancia'),
    ]

    titulo = forms.CharField(label='Titulo o palabras claves:', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese algo...'}))
    
    año = forms.ChoiceField(choices=AÑOS, widget=forms.Select(attrs={'class': 'form-control'}), required=False, label='Año:' )
    revista_o_provincial = forms.ChoiceField(choices=REVISTA_O_PROVINCIAL, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    instancia = forms.ChoiceField(choices=INSTANCIA_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    

class FormularioSentencia(forms.ModelForm):
    class Meta: 
        model = Sentencia
        fields = ['titulo', 'descripcion', 'revista_o_provincial', 'instancia', 'fecha', 'a_quien_aplica']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el titulo de la sentencia...'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escriba alguna descripción de la sentencia...'}),
            'revista_o_provincial': forms.Select(attrs={'class': 'form-control'}),
            'instancia': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'a_quien_aplica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A quien aplica...'}),
        }