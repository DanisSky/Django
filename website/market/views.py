from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views.generic import ListView

from account.models import Account
from cart.forms import CartAddProductForm
from .models import Category, Product, ProductReview


# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#
#     context = {'category': category,
#                'categories': categories,
#                'products': products}
#
#     return render(request, 'market/product/list.html', context)

class ProductListViewByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'market/product/list.html'

    def get_queryset(self):
        return Product.objects.filter(Q(available=True) & Q(stock__gt=0))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListViewByCategory, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context['category'] = category
        context['products'] = context['products'].filter(category=category)

        return context


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'market/product/list.html'

    def get_queryset(self):
        return Product.objects.filter(Q(available=True) & Q(stock__gt=0))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


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
