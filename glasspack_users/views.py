from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import UserLoginForm, UserPasswordChangeForm, UserRegistrationForm, UserProfileForm, UserPasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class UserRegistrationCreateView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'glasspack_users/registration.html'
    success_url = reverse_lazy('glasspack_users:register_done')


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = "glasspack_users/login.html"

    def get_success_url(self):
        return reverse_lazy("home")


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'glasspack_users/profile.html'

    def get_success_url(self):
        return reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "glasspack_users/password_change.html"
    success_url = reverse_lazy("glasspack_users:password_change_done")
    form_class = UserPasswordChangeForm


def register_done(request):
    return render(request, 'glasspack_users/register_done.html')

