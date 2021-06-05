from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from account import views
from account.forms import UserSignInForm
from account.views import profile, signup, verify

app_name = 'account'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
                                                authentication_form=UserSignInForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/registration/logged_out.html'), name='logout'),
    path('confirm/<str:code>', verify, name='verify'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('account:password_reset_complete'),
                                                     template_name="account/registration/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path("password_reset/", views.password_reset_request, name="password_reset")
]
