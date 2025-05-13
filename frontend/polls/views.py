import requests as req
import uuid
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout


def index(request):
    # Si el usuario no está autenticado, redirige a la página de login
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

@csrf_exempt
def login_view(request):
    # Si el usuario ya está autenticado, redirige a la página de inicio
    if request.method == 'POST':

        # Obtiene el nombre de usuario y la contraseña del formulario
        email = request.POST['email']
        password = request.POST['password']

        # Intenta validar las credenciales del usuario
        response = req.post(
            'http://localhost:5000/auth',
            json = {'email': email, 'password': password})

        # Si la respuesta es exitosa, autentica al usuario
        if response.status_code == 200:

            user_data = response.json()["data"]

            print(user_data)

            # Crea un nuevo usuario temporal (Con un ID temporal unico [email+uuid])
            temp_id = f"user_{user_data['email']}_{uuid.uuid4().hex[:6]}"
            user = User.objects.create_user(
                username=temp_id,
                email=user_data['email'],
                password=None
            )

            user.set_unusable_password()
            user.is_active = True
            user.save()

            request.session['user_id'] = user.id
            #request.session['role'] = user_data['role']
            #if request.user.role == 'soporte':
            

            login(request, user)

            return redirect('home')




    # Si el método no es POST, solo muestra el formulario
    return render(request, 'login.html')