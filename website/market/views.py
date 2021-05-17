from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from account.models import Account
from cart.forms import CartAddProductForm
from .models import Category, Product, ProductReview


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'category': category,
               'categories': categories,
               'products': products}

    return render(request, 'market/product/list.html', context)


def product_detail(request, id_, slug):
    product = get_object_or_404(Product,
                                id=id_,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 3)
        text = request.POST.get('content', '')
        account = get_object_or_404(Account, user_id=request.user.pk)
        ProductReview.objects.create(product=product, user=account,
                                     stars=stars, text=text)

        return redirect('market:product_detail', id_=id_, slug=slug)

    context = {'product': product,
               'cart_product_form': cart_product_form}

    return render(request, 'market/product/detail.html', context)
