from django.shortcuts import render, redirect, get_object_or_404, reverse

from django.contrib.auth import login, logout, authenticate
from .models import UsuarioBase, Juez, Lector, Sentencia
from .forms import FormularioSentencia, IngresoCustom, CreacionUsuarioCustom, FiltradoSentencias

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator


# Create your views here.
def signup_view(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': CreacionUsuarioCustom()})
    else:
        form = CreacionUsuarioCustom(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    user = form.save(commit=False)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.tipo = form.cleaned_data['tipo']
                    user.save()
                    login(request, user)  # Guarda la sesión usando las cookies
                    return redirect('home')
                except Exception as e:
                    return render(request, 'signup.html', {'form': form, 'error': f'El nombre de usuario ya existe o {e}.'})
            else:
                return render(request, 'signup.html', {'form': form, 'error': 'Las contraseñas no coinciden.'})
        else:
            return render(request, 'signup.html', {'form': form, 'error': 'Debe completar las casillas correctamente.'})

def signin_view(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': IngresoCustom()})
    else:
        form = IngresoCustom(request.POST)
        
        try:
                    user = authenticate(username=request.POST['username'], password=request.POST['password'])
                    # verifica el nombre de usuario y la contraseña y obtiene al usuario
                    
                    if user is None: # si no guardo nada, es que no se encontro el usuario
                        return render(request, 'signin.html', {'form': IngresoCustom(), 'error': 'La contraseña o el usuario es incorrecto'})
                    else:
                        login(request, user)
                        return redirect('home')
        except Exception as e:
                    return render(request, 'signup.html', {'form': form, 'error': f'El nombre de usuario ya existe o {e}.'})

@login_required
def logout_(request):
    logout(request)
    return redirect('signin')

@login_required
def home_view(request):
    form = FiltradoSentencias(request.POST or None)  # Si viene como POST obtenemos los datos, de lo contrario se crea el formulario para mostrar
    sentencias_list = Sentencia.objects.all()  # Todas las sentencias sin filtros

    if request.method == 'POST':
        # Filtrar por título (si se ha proporcionado)
        titulo = form.data.get('titulo')
        if titulo:
            sentencias_list = sentencias_list.filter(titulo__icontains=titulo)

        # Filtrar por año (si no se seleccionó "todos")
        año = form.data.get('año')
        print(año)
        if año and año != 'todos':
            sentencias_list = sentencias_list.filter(fecha__year=año)

        # Filtrar por revista o provincial
        revista_o_provincial = form.data.get('revista_o_provincial')
        print(revista_o_provincial)
        if revista_o_provincial and revista_o_provincial != 'todos':
            sentencias_list = sentencias_list.filter(revista_o_provincial=revista_o_provincial)

        # Filtrar por instancia
        instancia = form.data.get('instancia')
        print(instancia)
        if instancia and instancia != 'todos':
            sentencias_list = sentencias_list.filter(instancia=instancia)

    # Paginación
    paginator = Paginator(sentencias_list, 7)  # 7 sentencias por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'form': form, 'page_obj': page_obj})



@login_required
def create_sentence_view(request):
    if request.user.tipo == 'lector': # dado caso que un usuario lector entre se bloqueda desde código
            return HttpResponseForbidden("No tienes permiso para ver esta página.")
    if request.method == 'GET':
        return render(request, 'CrearSentencia.html', {'form':FormularioSentencia(), 'page': 1})
    else:
        form = FormularioSentencia(request.POST)
        if form.is_valid():
            sentencia = form.save(commit=False)
            sentencia.user = request.user  # Asigna el usuario autenticado al campo 'user'
            sentencia.save()
            return redirect('home')
        return redirect('home')

@login_required
def sentence_view(request, id):
    sentencia = get_object_or_404(Sentencia, id_sentencia=id)
    return render(request, "view_sentence.html", {'sentencia': sentencia})