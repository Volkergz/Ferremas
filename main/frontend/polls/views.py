from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'home.html', {
        'title': 'Polls Index',
        'message': 'Welcome to the Polls Index Page!'
    })

def login(request):
    return render(request, 'login.html', {
        'title': 'Login Page',
        'message': 'Please log in to continue.'
    })


