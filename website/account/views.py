from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.forms import UserSignUpForm


def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()

            return redirect('market:product_list')
    else:
        form = UserSignUpForm()

    return render(request, 'account/registration/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'account/profile.html', {'section': 'profile'})
