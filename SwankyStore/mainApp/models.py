from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    price = models.FloatField(max_length=10)
    stock = models.IntegerField()
    image = models.ImageField(upload_to="product_pictures/")
    discount_percent = models.IntegerField(default=0)

    
    def __str__(self) -> str:
        return self.title
