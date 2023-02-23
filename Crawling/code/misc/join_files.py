import pandas as pd 

reviews = pd.read_excel('shopee_reviews.xlsx')
products =pd.read_excel("shopee_products.xlsx")
shops = pd.read_excel("shopee_shops.xlsx")

products.rename(columns={column_name:f"product.{column_name}" if column_name not in ["shopid","itemid"] else column_name for column_name in list(products.columns)}, inplace=True)
shops.rename(columns={column_name:f"shop.{column_name}" if column_name!="shopid" else column_name for column_name in list(shops.columns)}, inplace=True)

result = pd.merge(reviews,products,on=['shopid','itemid'], how='left')
result = pd.merge(result,shops,on='shopid', how='left')
result.to_excel(f'merged.xlsx', index=False)
# print(result.head())