from django.shortcuts import render
from django.core.mail import send_mail

from computer_store.settings import DEFAULT_FROM_EMAIL
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

            send_mail(subject='Successful Order Message',
                      message=f"""
You have successfully created an order on Телефончик.by
Total price {cart.get_total_price_after_discount()} BYN
Our experts will contact you shortly
Have a nice day!
            """,
                      recipient_list=[order_request.user.email],
                      from_email=DEFAULT_FROM_EMAIL
                      )
            cart.clear()
            return render(request, 'orders/created.html',
                          {'order': order_request})
    else:
        form = OrderCreateForm
    return render(request, 'orders/create.html',
                  {'cart': cart, 'form': form})
