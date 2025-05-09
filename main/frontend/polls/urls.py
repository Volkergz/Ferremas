from django.urls import path
from . import views
from django.conf.urls import handler404


urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('', views.index, name='home'),
]


handler404 = 'polls.views.custom_404'