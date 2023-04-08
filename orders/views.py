from django.shortcuts import render
from django.views.generic import ListView

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():


            order_request = form.save(commit=False)  # Создаем объект, но не сохраняем его в БД
            order_request.user = request.user  # Указываем пользователя в поле person

            if cart.coupon:
                order_request.coupon = cart.coupon
                order_request.discount = cart.coupon.discount

            order_request.save()

            for item in cart:
                OrderItem.objects.create(order=order_request,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders/created.html',
                          {'order': order_request})
    else:
        form = OrderCreateForm
    return render(request, 'orders/create.html',
                  {'cart': cart, 'form': form})
