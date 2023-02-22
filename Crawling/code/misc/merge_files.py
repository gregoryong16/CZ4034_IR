import pandas as pd

# csv files in the path
# file_list = ["shopee_products_Computers-Peripherals-cat.11013247.xlsx","shopee_products_Home-Living-cat.11000001.xlsx"]
# dtype={'shopid': str,'itemid':str, 'rating':str, 'items_sold':str}

file_list =["shopee_shops_Computers-Peripherals-cat.11013247.xlsx","shopee_shops_Home-Living-cat.11000001.xlsx"]
dtype={'shopid': str,'userid':str}
# list of excel files we want to merge.
# pd.read_excel(file_path) reads the excel
# data into pandas dataframe.
excl_list = []

for file in file_list:
    excl_list.append(pd.read_excel(file, dtype=dtype))
 
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
excl_merged.to_excel('shopee_shops.xlsx', index=False)