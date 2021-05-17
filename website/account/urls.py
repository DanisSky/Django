from django.contrib.auth import views as auth_views
from django.urls import path

from account.views import profile, signup, verify

app_name = 'account'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/registration/logged_out.html'), name='logout'),
    path('confirm/<str:code>', verify, name='verify'),

]
