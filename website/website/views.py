from django.shortcuts import render


def custom_404(request, *args, **kwargs):
    print(args)
    print(kwargs)
    return render(request, 'errors/404_page.html', status=404)


def custom_500(request, *args, **kwargs):
    return render(request, 'errors/500_page.html', status=500)


def custom_403(request, *args, **kwargs):
    return render(request, 'errors/403_page.html', status=403)
