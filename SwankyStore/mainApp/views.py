from django.shortcuts import render, redirect
from . import models
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from custom_user.models import User
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from mainApp.models import Product, Cart, CartItem
from decimal import Decimal
from django.views.decorators.cache import never_cache


# Create your views here.

@never_cache
def index(request):
    product_list = None

    if request.method == 'POST':
        search_key = request.POST.get('search_key')
        product_list = Product.objects.filter(title__icontains=search_key)
    else:
        product_list = Product.objects.all()

    for product in product_list:
        if product.discount_percent != 0:
            product.new_price = calculate_discounted_price(product.price, product.discount_percent)

    cart_count = get_cart_items_count(request.user)

    product_and_other_context = {
        "products": product_list,
        "cart_count": cart_count
    }

    return render(request, 'mainApp/home.html', context=product_and_other_context)

@never_cache
def discounts(request):
    discounted_products = models.Product.objects.exclude(discount_percent=0)
    
    for product in discounted_products:
        product.new_price = calculate_discounted_price(product.price, product.discount_percent)

    cart_count = get_cart_items_count(request.user)

    products_and_other_context = {
        'products': discounted_products,
        'cart_count': cart_count}
    
    return render(request, 'mainApp/discounts.html', context=products_and_other_context)

@login_required(login_url="/login")
def my_cart(request):
    user_cart_items = CartItem.objects.filter(cart__user=request.user)

    cart_count = get_cart_items_count(request.user)
    cart_total = 0
    cart_actual_total = 0
    total_discount = 0

    for item in user_cart_items:
        # if the product is on sale ->
        actual_price = 0
        product = item.product
        

        if product.discount_percent > 0:
            actual_price = calculate_discounted_price(product.price, product.discount_percent)
            total_discount += (round(product.price, 3) - actual_price) * item.quantity
            product.new_price = actual_price
        else:
            actual_price = product.price

        cart_total += product.price * item.quantity

        item.total_price = (round(Decimal(actual_price * item.quantity), 3))
        cart_actual_total += item.total_price
            

    context = {'cart_items': user_cart_items,
               'cart_count': cart_count,
               'cart_total': round(Decimal(cart_total), 3),
               'cart_actual_total': round(Decimal(cart_actual_total), 3),
               'total_discount': round(Decimal(total_discount), 3)}
    
    return render(request, 'mainApp/my_cart.html', context)

def about(request):
    cart_count = get_cart_items_count(request.user)
    cart_context = {
        'cart_count':cart_count
    }
    return render(request, 'mainApp/about.html', context=cart_context)

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

@never_cache
def payment(request):
    user_cart_items = CartItem.objects.filter(cart__user=request.user)

    if not user_cart_items.exists():
        return redirect('mainApp:index')


    cart_count = get_cart_items_count(request.user)
    cart_actual_total = 0
    total_discount = 0

    for item in user_cart_items:
        # if the product is on sale ->
        actual_price = 0
        product = item.product
        
        if product.discount_percent > 0:
            actual_price = calculate_discounted_price(product.price, product.discount_percent)
            total_discount += (round(product.price, 3) - actual_price) * item.quantity
            product.new_price = actual_price
        else:
            actual_price = product.price

        user_name = request.user.username
        email = request.user.email

        item.total_price = (round(Decimal(actual_price * item.quantity), 3))
        cart_actual_total += item.total_price

    payment_context = {
        'cart_items': user_cart_items,
        'cart_count': cart_count,
        'cart_actual_total': round(Decimal(cart_actual_total), 3),       
        'total_discount': round(Decimal(total_discount), 3),
        'username': user_name,
        'email': email}              

    return render(request, 'mainApp/payment.html', context=payment_context)

def result(request):
    cart = Cart.objects.get(user = request.user)
    cart.delete()

    return render(request, 'mainApp/result.html')


# TRANSACTIONS ->

def search():
    pass

def calculate_discounted_price(price, discount_percent):
    discount_amount = (price * discount_percent) / 100
    discounted_price = price - discount_amount

    return round(discounted_price, 3)

@login_required(login_url="/login")
def add_to_cart(request):
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        page_name = request.POST.get('page_name')
        
        save_product_to_cart(request.user, product_id)

        return redirect(reverse(f'mainApp:{page_name}'))
    else:
        return redirect(reverse('mainApp:index'))
    
def save_product_to_cart(user, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

def get_cart_items_count(user):
    if user.is_authenticated:
        user_cart_items = CartItem.objects.filter(cart__user=user)
        item_count = 0
        for item in user_cart_items:
            item_count += item.quantity
        return item_count
    else:
        return None

def change_product_quantity(request):

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        transaction = request.POST.get('transaction')

        product = get_object_or_404(Product, id=product_id)

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            if transaction == 'remove':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
            elif transaction == 'add':
                cart_item.quantity += 1
                cart_item.save()
            return redirect(reverse('mainApp:my_cart'))    
        else:
            return redirect(reverse('mainApp:index'))
        
def delete_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(user = request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
    
        cart_item.delete()
        return redirect(reverse('mainApp:my_cart'))
    else:
        return redirect(reverse('mainApp:index'))

