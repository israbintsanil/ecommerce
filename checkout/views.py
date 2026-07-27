from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from shopping_cart.models import CartItem
from orders.models import Order, OrderItem


@login_required
def checkout(request):

    cart_items = CartItem.objects.filter(user=request.user)

    total = sum(item.total_price() for item in cart_items)

    if request.method == "POST":

        order = Order.objects.create(
            customer=request.user,
            total_amount=total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()

        return redirect("order_success")

    return render(request, "checkout/checkout.html", {
        "cart_items": cart_items,
        "total": total,
    })


def order_success(request):
    return render(request, "checkout/success.html")