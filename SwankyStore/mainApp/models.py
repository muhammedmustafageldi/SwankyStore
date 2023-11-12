from django.db import models
from custom_user.models import User

class Product(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    price = models.FloatField(max_length=10)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="product_pictures/")
    discount_percent = models.IntegerField(default=0)
    new_price = 0

    
    def __str__(self) -> str:
        return self.title


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Product', through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = 0

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in cart for {self.cart.user.username}"
