from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout  #usa el modelo de autenticación de Django
from django.contrib.auth.models  import User
from django.contrib import messages
from django.shortcuts import render

def index(request):
    # Si el usuario no está autenticado, redirige a la página de login
    # if not request.user.is_authenticated:
    #    return redirect('login')
    return render(request, 'home.html')

# Vista de registro de usuario
def register_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password'] 
        # Verifica si el usuario ya existe en la base de datos
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")  # Muestra error si existe
        else:
            # Crea un nuevo usuario
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Usuario registrado exitosamente")
            return redirect('login')  # Redirige a la página de login tras registrar
    # Si el método no es POST, solo muestra el formulario
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Credenciales incorrectas")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def catalogo_view(request):
    numeros = range(24)
    return render(request, 'Catalogo.html', {'numeros':numeros})





