from django.shortcuts import render
from django.http import HttpResponse
from . import models

# Create your views here.

def index(request):
    product_list = models.Product.objects.all()
    product_context = {"products":product_list}
    return render(request, 'mainApp/home.html', context=product_context)

def discounts(request):
    return render(request, 'mainApp/discounts.html')

def my_cart(request):
    return render(request, 'mainApp/my_cart.html')

def about(request):
    return render(request, 'mainApp/about.html')