from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import CartItem
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')


def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.total_price()

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })


def remove_from_cart(request, id):
    item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect('cart_view')


def increase_quantity(request, id):
    item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('cart_view')


def decrease_quantity(request, id):
    item = get_object_or_404(
        CartItem,
        id=id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect('cart_view')