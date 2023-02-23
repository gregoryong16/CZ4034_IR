import pandas as pd

# csv files in the path
# file_list = ["shopee_products_Computers-Peripherals-cat.11013247.xlsx","shopee_products_Home-Living-cat.11000001.xlsx"]
# dtype={'shopid': str,'itemid':str, 'rating':str, 'items_sold':str}
categories = ["Computers-Peripherals-cat.11013247","Home-Living-cat.11000001","Beauty-Personal-Care-cat.11012301","Home-Appliances-cat.11027421","Mobile-Gadgets-cat.11013350"]
# file_list =["shopee_shops_Computers-Peripherals-cat.11013247.xlsx","shopee_shops_Home-Living-cat.11000001.xlsx"]
dtype={'shopid': str,'itemid':str, 'rating':str, 'items_sold':str,'userid':str}
# dtype={'shopid': str,'userid':str}
# list of excel files we want to merge.
# pd.read_excel(file_path) reads the excel
# data into pandas dataframe.
excl_list = []
prefix = "shopee_products"
for category in categories:
    file = f"{prefix}_{category}.xlsx"
    excl_list.append(pd.read_excel(file,dtype=dtype))
 
# create a new dataframe to store the
# merged excel file.
excl_merged = pd.DataFrame()
 
for excl_file in excl_list:
     
    # appends the data into the excl_merged
    # dataframe.
    excl_merged = excl_merged.append(
      excl_file, ignore_index=True)
 
# exports the dataframe into excel file with
# specified name.
# excl_merged = excl_merged.dropna(subset=['comment'])
excl_merged.to_excel(f'{prefix}.xlsx', index=False)