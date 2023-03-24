from django.db import models

# Create your models here.
class Products(models.Model):
    shop_id = models.CharField(max_length = 20, null=True)
    item_id = models.CharField(max_length = 20, null=True)
    product_url = models.URLField(max_length = 200,null=True)
    product_name = models.CharField(max_length=400,null=True)
    product_price=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image_url = models.URLField(max_length = 200, null= True)
    shop_location = models.CharField(max_length=100,null=True)
    shop_name = models.CharField(max_length=100, null= True)

    # class Meta:
    #     app_label = 'indexing_project'

    def __str__(self):
        return self.product_name
                 
    objects = models.Manager()

