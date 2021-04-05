from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from cart.cart import Cart
from order.form import OrderCreateForm
from order.models import OrderItem, Order


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()

            return render(request, 'created.html',
                          {'order': order})
    else:
        form = OrderCreateForm

    return render(request, 'create.html',
                  {'cart': cart, 'form': form})
