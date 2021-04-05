from django.conf.urls import url

from account import views

app_name = 'account'

urlpatterns = [
    url('sign_up', views.sign_up, name='sign_up'),
    url('sign_in', views.sign_in, name='sign_in'),
]
