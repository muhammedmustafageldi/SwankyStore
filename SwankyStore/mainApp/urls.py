from django.urls import path
from . import views

app_name = 'mainApp'

urlpatterns = [
    path("", view= views.index, name="index"),
    path("discounts/", view=views.discounts, name="discounts"),
    path("myCart/", view=views.my_cart, name="my_cart"),
    path("about/", view=views.about, name="about")
]