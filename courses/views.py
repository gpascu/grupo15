from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Course, UserCourse
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm  # Importa il AuthenticationForm
import json
from django.shortcuts import render
from .forms import CourseFilterForm, RegistrarForm, ContactoForm
from datetime import datetime
from django.contrib.auth.models import User #agregado 22 octubre
from django.contrib import messages #AGREGADO 22 OCTUBRE
from .forms import UserRegistrationForm#agregado 22 octubre


def index(request):
    current_date = datetime.now()
    text_date = 'Fecha actual:'
    text_hour = 'Hora:'
    return render(request, 'index.html', {'date': current_date, 'text_date': text_date, 'text_hour': text_hour})

def contacto_form(request):
    print(request.POST)    
    if request.method == 'POST':
       formulario = ContactoForm(request.POST)
       if formulario.is_valid():
           return redirect('')
    else:
        formulario = ContactoForm()        
    contexto = {
        'contacto_form': formulario
    }
    return render(request, "contacto.html", contexto)

def signup(request):
    # Gestiona la logica de registraciòn
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

#inicio 22 octubre
def registro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password == password2:
                # Controla si el usuario ya existe
                if User.objects.filter(username=email).exists():
                    messages.error(request, 'Este usuario ya existe.')
                else:
                    # Crea el usuario
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.first_name = name
                    user.last_name = lastname
                    user.save()

                    messages.success(request, 'Usuario registrado exitosamente.')
                    return redirect('index')  # Redirecciona a otra pàagina una vez que se registra
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registro.html', {'form': form})
#----------fin22 octubre


def user_login(request):
    # Gestiona la logica de login
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirecciona si el login fue bueno
            return redirect('courseAvailable')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# @login_required
def course_list(request):
    # Devuelve lista cursos
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

# @login_required
def course_detail(request, course_id):
    # Devuelve detalles del curso
    course = Course.objects.get(pk=course_id)
    return render(request, 'course_detail.html', {'course': course})

def course_foro(request):
    #  Devuelve detalles del curso
    foro = Course.objects.all()
    return render(request, 'foro.html', {'foro': foro})

def course_register(request):
    #  Devuelve detalles del curso
    register = Course.objects.all()
    return render(request, 'registro.html', {'register': register})

def course_contact(request):
    #  Devuelve detalles del curso
    contact = Course.objects.all()
    return render(request, 'contacto.html', {'contact': contact})

@login_required
def course_available(request):
    #  Devuelve detalles del curso
    courseAvailable = Course.objects.all()
    return render(request, 'cursos.html', {'courseAvailable': courseAvailable})

