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

# # Reading excel files
# df = read_excel("../shopee_review_product_shop_combined.xlsx",sheet_name = "Sheet1")
# print(df.head()) # print the first 5 rows

# # Creating Objects using excel data
# for dbframe in df.itertuples():
#     print(dbframe[0])
#     obj = Products.objects.create(shop_id = dbframe[1], item_id = dbframe[2],time=dbframe[3],username=dbframe[4],comment=dbframe[5],
#                                   rating_star=dbframe[6], template_tags=dbframe[7],product_url=dbframe[8], name=dbframe[9], 
#                                   original_price=dbframe[10], current_price=dbframe[11],description=dbframe[12], rating=dbframe[13], 
#                                   image_url=dbframe[14],items_sold=dbframe[15],category=dbframe[16], total_rating=dbframe[17], 
#                                   user_id=dbframe[18], shop_place=dbframe[19],shop_location=dbframe[20], item_count=dbframe[21],
#                                   shop_ratings=dbframe[22], shop_response_rate=dbframe[23],shop_name=dbframe[24], 
#                                   shop_response_time=dbframe[25], shop_follower_count=dbframe[26],shop_rating_bad=dbframe[27],
#                                   shop_rating_good=dbframe[28],shop_rating_normal=dbframe[29],shop_username=dbframe[30])          
#     obj.save()

print(Products.objects.filter(name__startswith='SG'))
