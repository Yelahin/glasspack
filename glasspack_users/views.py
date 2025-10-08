from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import UserLoginForm
from glasspack_site.utils import menu

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            
    else:
        form = UserLoginForm()

    return render(request, 'glasspack_users/login.html', {"form": form, "menu": menu})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('glasspack_users:login'))