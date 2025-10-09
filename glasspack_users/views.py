from django.urls import reverse_lazy
from .forms import UserLoginForm
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = "glasspack_users/login.html"

    def get_success_url(self):
        return reverse_lazy("home")
    