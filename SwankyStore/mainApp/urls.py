from django.urls import path
from . import views

app_name = 'mainApp'

urlpatterns = [
    path("", view= views.index, name="index"),
    path("discounts/", view=views.discounts, name="discounts"),
    path("myCart/", view=views.my_cart, name="my_cart"),
    path("about/", view=views.about, name="about"),
    path("sign_up/", view=views.sign_up, name="sign_up"),
    path("add_to_cart/", view=views.add_to_cart, name="add_to_cart"),
    path("change_product_quantity/", view=views.change_product_quantity, name="change_product_quantity"),
    path("delete_product/", view=views.delete_product, name='delete_product'),
    path("payment/", view=views.payment, name='payment'),
    path("result/", view=views.result, name='result'),
]