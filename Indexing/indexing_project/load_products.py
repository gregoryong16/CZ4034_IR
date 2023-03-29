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

## Reading excel files
df = read_excel(BASE_DIR+"/shopee_product_shop_combined.xlsx",sheet_name = "Sheet1")
print(df.head()) # print the first 5 rows

# Creating Objects using excel data
for dbframe in df.itertuples():
    print(dbframe[0])
    obj = Products.objects.create(shop_id = dbframe[2], item_id = dbframe[3],product_url=dbframe[1], product_name=dbframe[4], 
                                  product_price=dbframe[7], description=dbframe[8], rating=dbframe[9], 
                                  image_url=dbframe[10], shop_location=dbframe[14], shop_name=dbframe[15])          
    obj.save()
