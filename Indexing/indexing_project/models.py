from django.db import models

# Create your models here.
class Products(models.Model):
    name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    ratings = models.DecimalField(max_digits=3, decimal_places=1)
    image_url = models.URLField(max_length = 200)
    shop_id = models.CharField(max_length = 500)
    item_id = models.CharField(max_length = 500)

    def __str__(self):
        return self.name
                 
    objects = models.Manager()

