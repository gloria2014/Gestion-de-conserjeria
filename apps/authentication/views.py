
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
#from django.db import connection
from apps.authentication.models import Region, Comuna
from .forms import LoginForm, SignUpForm
import logging
from django.http import JsonResponse, HttpResponse

# Copyright 2001-2022 by Vinay Sajip. All Rights Reserved.
logger = logging.getLogger(__name__)


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Credenciales inválidas'
        else:
            msg = 'Error al validar el formulario'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

# REGISTRO DE USUARIOS 
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def logout_user(request):
    logout(request)
    return redirect("/login/")


def listar_empleados(request):
    # Aquí iría la lógica para obtener la lista de empleados
    empleados = []  # Reemplaza esto con la lógica real

    context = {
        'empleados': empleados,
        'submenu_open': True,  # Asegúrate de incluir esta clave
        'segment': 'listar-empleados'  # Incluye también esta clave
    }
    
    return render(request, 'home/listar-empleados.html', context)


