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

def cambiarMoneda(request):
    # Verifica si el método de la solicitud es POST
    if request.method == 'POST':
        # Obtiene la moneda seleccionada desde el formulario
        moneda = request.POST.get('moneda')
        # Almacena la moneda en la sesión
        request.session['moneda'] = moneda
        # Redirige a la página de inicio
        return redirect('home')
    
    # Si no es un método POST, redirige a la página de inicio
    return redirect('home')

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
            request.session['username'] = user_data['nombres']
            request.session['role'] = user_data['id_rol']     

            login(request, user)

            # Redirige a la página de inicio de usuario tras iniciar sesión
            return redirect('home')

    # Si el método no es POST, solo muestra el formulario
    return render(request, 'login.html')

def catalogo_view(request):

    # Verifica la moneda seleccionada
    moneda = request.session.get('moneda')

    # Si no hay moneda seleccionada, establece una por defecto
    if not moneda:
        moneda = 'CLP'
        request.session['moneda'] = moneda

    # Solicita la lista de productos a la API
    response = req.post('http://localhost:5001/productos')

    # Si la respuesta es exitosa, se obtiene la lista de productos
    if response.status_code == 200:

        # Si la moneda no es USD, guarda los productos directamente
        if moneda != 'USD':
            items = response.json()

        else:
            # Si la moneda es USD, realiza una solicitud a la API para obtener el valor del dólar
            res = req.get('http://localhost:5003/getDollar')

            # Si la respuesta es exitosa, se obtiene el valor del dólar
            if res.status_code == 200:

                # Extrae el valor del dólar de la respuesta
                usd = res.json().get('dollar_value')
                print(usd)


                # Si el valor del dólar es válido, convierte los precios
                if usd and usd > -1:

                    # Convierte los precios de los productos a USD
                    items_data = response.json()

                    # Convierte los precios de CLP a USD
                    for item in items_data:
                        item['precio'] = round(item['precio'] / usd, 2)
                    
                    # Almacena los productos convertidos en la variable items
                    items = items_data
                else:
                    messages.error(request, "Tasa de cambio no válida.")
                    items = []
    else:
        items = []

    # Paginación de los productos
    paginator = Paginator(items, 16) # 16 productos por página
    page_number = request.GET.get('page') # Obtiene el número de página actual
    page_obj = paginator.get_page(page_number) #Obtiene los productos de la página actual

    # Renderiza la plantilla con los productos paginados
    return render(request, 'Catalogo.html', {
        'page_obj': page_obj
    })

def cambiarMoneda(request):
    try:
        # Obtener la moneda actual
        moneda = request.session.get('moneda')

        # Alternar la moneda
        if moneda == 'USD':
            request.session['moneda'] = 'CLP'
        elif moneda == 'CLP':
            request.session['moneda'] = 'USD'
        else:
            request.session['moneda'] = 'USD'

        # Redirige a la página anterior si existe, si no, al home
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('home')
        
    except Exception as e:
        return redirect('home')


# Vista de cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('home')

def producto_view(request, id):

    # Realizamos una solicitud GET a la API para obtener los detalles del producto
    response = req.get(f'http://localhost:5001/productos/{id}')

    # Si la respuesta es exitosa, se obtiene el producto
    if response.status_code == 200:
        
        # Verifica la moneda seleccionada
        moneda = request.session.get('moneda')

        # Si no hay moneda seleccionada, establece una por defecto
        if not moneda:
            moneda = 'CLP'
            request.session['moneda'] = moneda

        producto = response.json()
        
        # Si la moneda es USD, realiza una solicitud a la API para obtener el valor del dólar
        if moneda == 'USD':
            # Si la moneda es USD, realiza una solicitud a la API para obtener el valor del dólar
            res = req.get('http://localhost:5003/getDollar')

            # Si la respuesta es exitosa, se obtiene el valor del dólar
            if res.status_code == 200:

                # Extrae el valor del dólar de la respuesta
                usd = res.json().get('dollar_value')

                # Si el valor del dólar es válido, convierte los precios
                if usd and usd > 0:
                    producto['precio'] = round(producto['precio'] / usd, 2)
                    
                else:
                    messages.error(request, "Tasa de cambio no válida.")
        
        # Renderiza la plantilla con los detalles del producto
        return render(request, 'producto.html', {'producto': producto})
    else:    
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

    #Verifica que este accediendo por el metodo GET
    if request.method == 'GET':
        
        # Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Realiza una solicitud GET a la API para obtener los productos del carrito
        response = req.get(f'http://localhost:5002/getOrden/{request.session.get("user_id")}')
        
        # Si la respuesta es exitosa, se obtiene el carrito
        if response.status_code == 200:
            productos = response.json()

            # Calcula el total del carrito
            total = sum(item['subtotal'] for item in productos)

            #Creamos un diccionario para almacenar el contexto
            contexto = {
                'productos': productos,
                'total': total
            }

            return render(request, 'carrito.html', contexto)
        
        # Si la respuesta no es exitosa, mostramos el carrito vacío
        return render(request, 'carrito.html')

    return render(request, 'carrito.html')

def removeItem(request, id_producto):
    if request.method == 'POST':
        id_usuario = request.session.get('user_id')

        if not id_usuario:
            messages.error(request, "Usuario no autenticado.")
            return redirect('carrito')

        # Llama al backend Flask
        response = req.delete(f'http://localhost:5002/removeItem/{id_producto}/{id_usuario}')

        if response.status_code == 200:
            return redirect('carrito')
        else:
            messages.error(request, "Error al eliminar el producto del carrito.")
            return redirect('carrito')
    
    return redirect('carrito')  # Por seguridad, redirige si acceden por otro método

def iniciarCompra(request):

    # Verifica si el usuario está autenticado
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para realizar un pago.")
        return redirect('login')
    
    # Verifica si la petición es POST
    if request.method != 'POST':
        messages.error(request, "Método no permitido.")
        return redirect('carrito')

    # Obtiene el ID del usuario desde la sesión
    id_usuario = request.session.get('user_id')

    # Obtiene el carrito del usuario
    response = req.get(f'http://localhost:5002/getDataOrden/{id_usuario}')

    # Si la respuesta es exitosa, se obtiene el carrito
    if response.status_code == 200:

        # Extrae los datos del carrito
        data = response.json()

        # Inicia la transacción
        res = req.post('http://localhost:5004/crear-transaccion', json=data)

        # Si la respuesta es exitosa, se obtiene el token y la URL
        if res.status_code == 200:
            response = res.json()
            token = response['token']
            url = response['url']
            return redirect(f'{url}?token_ws={token}')
        else:
            messages.error(request, "Error al iniciar la transacción.")
            return redirect('carrito')

    else:
        messages.error(request, "Error al obtener el carrito.")
        return redirect('carrito')

def confirmarCompra(request):
    # Verifica si la petición es GET
    if request.method != 'GET':
        messages.error(request, "Método no permitido.")
        return redirect('carrito')

    token = request.GET.get('token_ws')

    # Realiza una solicitud POST a la API para confirmar la transacción
    response = req.post('http://localhost:5004/confirmar-transaccion', json={'token_ws': token})

    # Si la respuesta es exitosa, se obtiene la respuesta
    if response.status_code == 200:
        response = response.json()

        print(response)

        # Verifica el estado de la transacción
        if response['status'] == 'AUTHORIZED':
            # Si la transacción fue autorizada, actualiza el estado de la orden
            id_orden = response['buy_order']
            id_usuario = request.session.get('user_id')

            # Realiza una solicitud POST a la API para actualizar el estado de la orden
            req.post(f'http://localhost:5002/cerrarCompra/{id_orden}/{id_usuario}')

            messages.success(request, "Compra realizada exitosamente.")
            
            # Redirige a la página de confirmación de compra
            #return redirect('confirmarCompra')
            return redirect('home')

        # Si la transacción no fue autorizada, muestra un mensaje de error
        else:
            messages.error(request, "La transacción no fue autorizada.")
            # Redirección a la pagina de error de pago
            redirect('carrito')
    else:
        # Redirección a la pagina de error de pago
        redirect('carrito')

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