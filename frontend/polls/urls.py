from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('producto/<int:id>', views.producto_view, name='producto'),
    path('carrito', views.carrito_view, name='carrito'),
    path('catalogo/', views.catalogo_view, name='catalogo'),
    path('', views.home, name="home")
]