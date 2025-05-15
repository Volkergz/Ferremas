from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout  #usa el modelo de autenticación de Django
from django.contrib.auth.models  import User
from django.contrib import messages
from django.shortcuts import render
from django.core.paginator import Paginator
import requests as req
from django.views.decorators.csrf import csrf_exempt
import uuid

# Vista de la página de inicio
def home(request):
    return render(request, 'home.html')

# Vista de inicio de sesión
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
            json = {'email': email, 'password': password}
        )

        # Si la respuesta es exitosa, autentica al usuario
        if response.status_code == 200:

            user_data = response.json()

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

            request.session['user_id'] = user_data['id_usuario']
            request.session['role'] = user_data['id_rol']     

            login(request, user)

            # Redirige a la página de inicio de admintración tras iniciar sesión
            #if user_data['id_rol'] == 1:
            #    return redirect('admin')

            # Redirige a la página de inicio de usuario tras iniciar sesión
            return redirect('home')

    # Si el método no es POST, solo muestra el formulario
    return render(request, 'login.html')

def catalogo_view(request):

    # Intenta validar las credenciales del usuario
    items = req.post('http://localhost:5001/productos')

    # Si la respuesta es exitosa, se obtiene la lista de productos
    if items.status_code == 200:
        items = items.json()
    else:
        items = []

    # Filtra los productos según los parámetros de búsqueda

    herramienta = request.GET.get('reemplazar')
    if herramienta:
        items = items.filter(herramienta__iexact=herramienta)

    precio = request.GET.get('reemplazar')
    if precio:
        min_price, max_price = map(int, precio.split('-'))
        items = items.filter(precio__gte=min_price, precio__lte=max_price)

    marca = request.GET.get('reemplazar')
    if marca:
        items = items.filter(marca__iexact=marca)

    # Paginación de los productos
    paginator = Paginator(items, 16) # 16 productos por página
    page_number = request.GET.get('page') # Obtiene el número de página actual
    page_obj = paginator.get_page(page_number) #Obtiene los productos de la página actual

    # Renderiza la plantilla con los productos paginados
    return render(request, 'Catalogo.html', {
        'page_obj': page_obj
    })

# Vista de cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('home')

def producto_view(request, id):

    # Realizamos una solicitud GET a la API para obtener los detalles del producto
    response = req.get(f'http://localhost:5001/productos/{id}')

    # Si la respuesta es exitosa, se obtiene el producto
    if response.status_code == 200:
        producto = response.json()

        # Renderiza la plantilla con los detalles del producto
        return render(request, 'producto.html', {
            'producto': producto
        })
    
    # Si la respuesta no es exitosa, redirige a la página de catálogo
    return redirect('catalogo')

def add_to_cart(request):
    # Verifica si el método de la solicitud es POST
    if request.method == 'POST':

        # Obtiene los datos desde la solicitud POST
        data = {
            'id_producto': int(request.POST.get('id_producto')),
            'id_usuario': int(request.session.get('user_id')),
            'cantidad': int(request.POST.get('cantidad'))
        }

        print(data)

        # Realiza una solicitud POST a la API para agregar el producto al carrito
        response = req.post('http://localhost:5002/addCar', json=data)

        # Si la respuesta es exitosa, redirige a la página del carrito
        if response.status_code == 200:
            return redirect('carrito')
        
        # Si la respuesta no es exitosa, redirige a la página de catálogo
        messages.error(request, "Error al agregar el producto al carrito")
        return redirect('catalogo')

    # Si no es un método POST, redirige a la página de catálogo
    return redirect('catalogo')

def carrito_view(request):
    return render(request, 'carrito.html')

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