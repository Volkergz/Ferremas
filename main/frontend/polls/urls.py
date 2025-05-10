from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('catalogo', views.catalogo_view, name='catalogo'),
    path('', views.index, name="home")
]