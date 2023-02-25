from django.db import models

# Create your models here.
class Products(models.Model):
    shop_id = models.CharField(max_length = 20, null=True)
    item_id = models.CharField(max_length = 20, null=True)
    time = models.CharField(max_length = 20, null=True)
    username = models.CharField(max_length=100,null= True)
    comment = models.TextField(blank=True, null=True)
    rating_star = models.IntegerField(null=True)
    template_tags = models.CharField(max_length=100,null=True)
    product_url = models.URLField(max_length = 200,null=True)
    name = models.CharField(max_length=400,null=True)
    original_price=models.CharField(max_length = 20, null=True)
    current_price=models.CharField(max_length = 20, null=True)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    image_url = models.URLField(max_length = 200, null= True)
    items_sold = models.CharField(max_length=100,null= True)
    category = models.CharField(max_length=100,null=True)
    total_rating = models.IntegerField(null=True)
    user_id = models.CharField(max_length = 20,null=True)
    shop_place = models.CharField(max_length=100,null=True)
    shop_location = models.CharField(max_length=100,null=True)
    item_count = models.IntegerField(null=True)
    shop_ratings = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    shop_response_rate = models.IntegerField(null=True)
    shop_name = models.CharField(max_length=100, null= True)
    shop_response_time = models.IntegerField(null=True)
    shop_follower_count = models.IntegerField(null=True)
    shop_rating_bad = models.IntegerField(null=True)
    shop_rating_good = models.IntegerField(null=True)
    shop_rating_normal = models.IntegerField(null=True)
    shop_username = models.CharField(max_length=100, null = True)

    # class Meta:
    #     app_label = 'indexing_project'

    def __str__(self):
        return self.name
                 
    objects = models.Manager()

