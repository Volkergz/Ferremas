from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('cambiarMoneda', views.cambiarMoneda, name='cambiarMoneda'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('producto/<int:id>', views.producto_view, name='producto'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('carrito', views.carrito_view, name='carrito'),
    path('carrito/removeItem/<int:id_producto>', views.removeItem, name='carrito/removeItem'),
    path('carrito/iniciarCompra', views.iniciarCompra, name='carrito/iniciarCompra'),
    path('carrito/confirmarCompra', views.confirmarCompra, name='carrito/confirmar_compra'),
    path('', views.home, name="home")
]