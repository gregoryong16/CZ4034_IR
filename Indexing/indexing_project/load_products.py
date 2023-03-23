# from .models import Products
from pandas import read_excel
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] =  "web_app.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_app.settings")
import django
django.setup()
from indexing_project.models import Products

# Reading excel files
df = read_excel("../shopee_review_product_shop_combined.xlsx",sheet_name = "Sheet1")
print(df.head()) # print the first 5 rows

# Creating Objects using excel data
for dbframe in df.itertuples():
    print(dbframe[0])
    obj = Products.objects.create(shop_id = dbframe[1], item_id = dbframe[2],product_url=dbframe[8], product_name=dbframe[9], 
                                  product_price=dbframe[12], description=dbframe[13], rating=dbframe[14], 
                                  image_url=dbframe[15], shop_location=dbframe[21],
                                  shop_ratings=dbframe[23],shop_name=dbframe[25])          
    obj.save()

print(Products.objects.filter(name__startswith='SG'))