from django.shortcuts import render, redirect
from . import models
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from custom_user.models import User
from django.contrib.auth import login



# Create your views here.

def index(request):
    product_list = models.Product.objects.all()

    for product in product_list:
        if product.discount_percent != 0:
            product.new_price = calculate_discounted_price(product.price, product.discount_percent)
            
    product_context = {"products":product_list}
    return render(request, 'mainApp/home.html', context=product_context)

def calculate_discounted_price(price, discount_percent):
    discount_amount = (price * discount_percent) / 100
    discounted_price = price - discount_amount

    return round(discounted_price, 3)

def discounts(request):
    discounted_products = models.Product.objects.exclude(discount_percent=0)
    
    for product in discounted_products:
        product.new_price = calculate_discounted_price(product.price, product.discount_percent)

    products_context = {'products': discounted_products}
    return render(request, 'mainApp/discounts.html', context=products_context)

@login_required(login_url="/login")
def my_cart(request):
    return render(request, 'mainApp/my_cart.html')

def about(request):
    return render(request, 'mainApp/about.html')

def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password_conf = request.POST["passwordConf"]
        
        # Is the username and email unique?
        if User.objects.filter(email = email).exists():
            error_message = 'There is already a registered user with this email.'
            return render(request, 'registration/sign_up.html', {'error_message':error_message})
        elif User.objects.filter(username = username).exists():
            error_message = 'There is already a user registered with this username.'
            return render(request, 'registration/sign_up.html', {'error_message':error_message})
        else:
            # Check if the passwords match
            if password == password_conf:
                user = User.objects.create_user(username = username, email = email, password = password)
                login(request, user)
                return redirect(reverse_lazy('mainApp:index'))
            else:
                error_message = 'Passwords do not match.'
                return render(request, 'registration/sign_up.html', {'error_message':error_message})    
        
    else:
        return render(request, 'registration/sign_up.html')

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        page_name = request.POST.get('page_name')
        
        print(product_id)
        return redirect(reverse(f'mainApp:{page_name}'))
    else:
        return redirect(reverse('mainApp:index'))