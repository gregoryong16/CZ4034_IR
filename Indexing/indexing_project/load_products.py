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

df = read_excel("shopee_review_product_shop_combined.xlsx",sheet_name = "Sheet1")
print(df.head()) # print the first 5 rows


# for dbframe in df.itertuples():
#     print(dbframe["product.name"])
#     obj = Products.objects.create(Empcode=dbframe.Empcode,firstName=dbframe.firstName, middleName=dbframe.middleName,
#                                     lastName=dbframe.lastName, email=dbframe.email, phoneNo=dbframe.phoneNo, address=dbframe.address,
#                                     gender=dbframe.gender, DOB=dbframe.DOB,salary=dbframe.Salary )           
    # obj.save()
# for row in range(1, worksheet.max_row+1):
#     for dbframe in worksheet[row].itertuples():
#         print(dbframe.product.name)
#         # obj = Products.objects.create(name=worksheet[i].value.product.name, description=worksheet[i].value.product.description)          
#         # obj.save()

# print(Products.objects.filter(name__startswith='SG'))
