from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'websites/index.html')