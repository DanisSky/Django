from django.shortcuts import render

# Create your views here.
from cart.cart import Cart
from order.form import OrderCreateForm
from order.models import OrderItem


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
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
