from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.views import LogoutView
from . import views

app_name = "glasspack_users"

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('sign_up/', views.UserRegistrationCreateView.as_view(), name='sign_up'),
    path('register_done/', views.register_done, name='register_done'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/',  PasswordChangeDoneView.as_view(template_name="glasspack_users/password_change_done.html"), name='password_change_done'),

]