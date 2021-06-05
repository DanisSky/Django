from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect

from account.forms import UserSignUpForm
from account.models import Account
from account.task import send_password_reset_email


def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']
                user.save()
            except IntegrityError:
                form.add_error('email', 'email is used')
                return render(request, 'account/registration/register.html', {'form': form})

            return redirect('market:product_list')
    else:
        form = UserSignUpForm()

    return render(request, 'account/registration/register.html', {'form': form})


def verify(request, code):
    try:
        user = Account.objects.get(verification_uuid=code, is_verified=False)
    except Account.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_verified = True
    user.save()

    return redirect('account:profile')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            user_email = password_reset_form.cleaned_data['email']
            send_password_reset_email(user_email)

            return redirect("account:password_reset_done")

    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="account/registration/password_reset.html",
                  context={"password_reset_form": password_reset_form})


@login_required
def profile(request):
    return render(request, 'account/profile.html', {'section': 'profile'})
