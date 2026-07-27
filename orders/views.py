from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by("-order_date")

    return render(request, "orders/my_orders.html", {
        "orders": orders
    })

# Create your views here.
