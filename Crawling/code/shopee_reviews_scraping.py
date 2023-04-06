from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
import sys, os
import random
from selenium.webdriver.common.action_chains import ActionChains
import cssutils
import re
import requests
import json

# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
def get_reviews_from_shopee_api(shopid,itemid,product):
  
  reviews = []
  try:
    offset=0
    ratings_number_scraped = False
    while True:
      # time.sleep(random.uniform(2, 4))
      # filter the reviews with comments
      url = f'https://shopee.sg/api/v2/item/get_ratings?filter=1&flag=1&itemid={itemid}&limit=50&offset={offset}&shopid={shopid}&type=0'
      # Make a request to the API
      response = requests.get(url)
      # Load the response JSON into a Python dictionary
      data = json.loads(response.text)
      # Extract the data you need from the dictionary
      results = data['data']['ratings']

      # scrape number of ratings
      if not ratings_number_scraped:
        item_rating_summary = data['data']['item_rating_summary']
        if item_rating_summary!=None:
          product.update(item_rating_summary)
          ratings_number_scraped = True
      if (results==None):
        break
      # oversea reviews shopid and itemid are different, needs to standardized
      # keys to select
      selected_keys = ["shopid","itemid","ctime","author_username","comment","rating_star","template_tags"]
      # selected_keys = []

      # if len(results)>0:
      #   selected_keys = list(results[0].keys())
      # create a new list of dictionaries with only selected keys
      new_results = [{key: shopid if key == 'shopid' else itemid if key == 'itemid' else d[key] for key in selected_keys} for d in results]

      # drop rows with no comments
      filtered_new_results = [d for d in new_results if d["comment"] != None and d["comment"].strip() != ""  ]
      if (len(new_results)==0):
        print('--- reviews results length 0---',url)
        break
      reviews.extend(filtered_new_results)


      offset+=len(new_results)
      if (len(reviews)>=50):
        break

  except Exception as e:
    print(e)

  return reviews

def get_shop_info_from_shopee_api(shopid):
  try:
    url = f"https://shopee.sg/api/v4/product/get_shop_info?shopid={shopid}"
    response = requests.get(url)
    # Load the response JSON into a Python dictionary
    data = json.loads(response.text)
    # Extract the data you need from the dictionary
    shop_info = data['data']
    if (shop_info==None):
      print("Results none:",url)
      return
    # oversea reviews shopid and itemid are different, needs to standardized
    # keys to select
    # selected_keys = ["shopid","userid","place","shop_location","item_count","rating_star","response_rate","name","response_time","follower_count","rating_bad","rating_good","rating_normal"]
    # create a new list of dictionaries with only selected keys
    # selected_shop_info = {key: shopid if key == 'shopid' else str(shop_info['userid']) if key == 'itemid' else shop_info[key] for key in selected_keys}
    # selected_shop_info["username"] =  shop_info["account"]["username"]
    # drop rows with no comments
    # return selected_shop_info
    return shop_info
  except Exception as e:
    print(e)

def get_item_from_shopee_api(shopid,itemid):
  try:
    headers = {
      'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
      'sz-token': 'Ra/NJSFhMbpYXlWXB/kMKw==|tbtAeRuQraLaHXP0PPLER62V4RREUxTHlM0sHpOnYMwbMMQeM9+qLgkomlUGpUVkjby5btMmGHCl9DFdTYOavUNJ3LuXv0sobg==|oZGZsgOMDe5oaMrE|06|3',
      'sec-ch-ua-mobile': '?0',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
      'Content-Type': 'application/json',
      'X-API-SOURCE': 'pc',
      'Accept': 'application/json',
      'X-Shopee-Language': 'zh-Hans',
      'X-Requested-With': 'XMLHttpRequest',
      'af-ac-enc-dat': 'AAcyLjQuMS0yAAABhE3Hy6UAAAtLAkIAAAAAAAAAAOYyhFAbVQMMpIKa2+dGIBkKaWUVkWOzjLDykZY2dhCO2aemll6zSawP7dqKio0tSXU8mzeKLk1kA/WyNZ3Ie5A5Nt4iJ1W9aNhMRfWeQ7v8d9m7rMmAzdpxzPCKsKZUt89X1xFf0TvL/NsDCZSiE3F0ERsJBPsctX1CYA4baakfSx+Mbik3yDbxzfoZ9uXVS6oq2etzh1XniTb6mLKOF6kwSZbxI4FnzTS4k+XtcD7yPyi9O9arrEYGHKDT1AgxhDj+TLRcJqaQNDvlDA7IiJvpFsgpeHQXx+lEECXlHknmoTTyj/Vn1dcMyFsj0rpApuO6LdYYfR0WvgE2pJEUSvIqWlCgTPpSIKBuWK+C0hzfGe1o4iEHKgzvRydrIs0DhQk1YcG18ylDmIpexxyWlfUaRjfn5DtSUG9QIVLUSI3R8+2Vi3kGkiVgGH5vlT424PFUtNdb+8K1kDEitmBAZRnJhX2FvN44sM3YZnxNQDhfDc5iLQNlRwi12gPtyiO0aJ0u0EHc6LpdriVstGniIcACAExdmmlMQ+JYTMHF6kF68iRD85aWYi9ro3Wl9b3oSySuEOrDBjHFr5rF050g933uBLbAAhpLfIO+hSPwGUPsJ9/+NzAlsFLDIzfdYGNDP9z6GA2N8G6rj84L/ADQ7yqJhWpZ4w6ktdU1QBJ19JM+JjxlMGGa5/CKeBxPVMGF0rhbVQGRY7OMsPKRljZ2EI7Zp6aWkWOzjLDykZY2dhCO2aemlhn+1ZL5DKAyhUWhwsV2anPVK717vjBfA5ZAs0C9mW0Z',
      'X-CSRFToken': 'IDq3287GJnXS5JJj5c2p5NfuvByGNpst',
      'sec-ch-ua-platform': '"Windows"',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Dest': 'empty',
      'host': 'shopee.sg',
      'Cookie': 'REC_T_ID=99d3d94f-5df0-11ed-b735-2cea7fa8daa9; SPC_F=w4AfWBkq1JrakV2jppFicIhTClRLblU7; SPC_R_T_ID=UXubTQvc/YPsM6xl+teVYis0dA2qLMfX6XkESPWMhmcIFaEi8LrMjdy7JotmJURfc8VtNc6ecvjQ5h0QxzshCQkSOwSRbEYbPzopwt27ggZispI0Ud4iKQQFka+NykFRJH0vM8M04lQUpSa5SxdHmdirR2k7laqgj3MTGLHCqTQ=; SPC_R_T_IV=R0Y1N1IwUUFYa1VqTjJRTw==; SPC_SI=m5xjYwAAAABKQ2FmemF6RlFAiQAAAAAARjNNa3hrdEw=; SPC_T_ID=UXubTQvc/YPsM6xl+teVYis0dA2qLMfX6XkESPWMhmcIFaEi8LrMjdy7JotmJURfc8VtNc6ecvjQ5h0QxzshCQkSOwSRbEYbPzopwt27ggZispI0Ud4iKQQFka+NykFRJH0vM8M04lQUpSa5SxdHmdirR2k7laqgj3MTGLHCqTQ=; SPC_T_IV=R0Y1N1IwUUFYa1VqTjJRTw=='
    }

    res = requests.get(f"https://shopee.sg/api/v4/item/get?itemid={itemid}&shopid={shopid}",headers=headers)
    return res.json()["data"]
  except Exception as e:
    print(e)  


def main(category):
  # set up the driver (make sure to download the appropriate driver for your browser)
  # driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe')
  rows = []
  products = []
  shops = []
  # reviews_pages_to_scrape = 2


  my_file = open(f"shopee_product_links_{category}.txt", "r" , encoding="utf-8" )
  data = my_file.read()
  urls = data.split("\n")
  my_file.close()

  # products_pages_to_scrape =2
  # def scrape_shopee_product_reviews(url):
  for index,url in enumerate(urls):
    # count=index+1
    # if count>products_pages_to_scrape:
    #   break
    print(index,url)
    # navigate to the Shopee product page
    # driver.get(url)

    # reviews_section_class = "shopee-product-rating__main"

    # product_title_class = "_44qnta"
    # # maybe image url, price , items sold and so on
    # original_price_class = "Y3DvsN"
    # current_price_class = "pqTWkA"
    # product_description_class = "f7AU53"

    # product_primary_image_class ="VWiifV qO2bZw"
    # product_secondary_image_class = "A4dsoy qO2bZw"
    # rating_class = "product-rating-overview__rating-score"
    # items_sold_class = "P3CdcB"
    # category_class = "akCPfg KvmvO1"

    # ELEMENTS_TO_SCRAPE = [{"name":"original_price", "class":original_price_class},{"name":"current_price", "class":current_price_class},{"name":"description", "class":product_description_class},{"name":"rating", "class":rating_class},{"name":"items_sold","class":items_sold_class}]


    try:
      # count=0
      
      match = re.search(r"i\.(\d+)\.(\d+)$", url)

      if match:
        shopid = match.group(1)
        itemid = match.group(2)
        # delay = random.uniform(3, 5)
        # time.sleep(delay)
        product = get_item_from_shopee_api(shopid,itemid)
        product["url"] = url
        # time.sleep(random.uniform(6, 10))
        new_shop = get_shop_info_from_shopee_api(shopid)
        if (new_shop):
          new_shop_exists = False
          for shop in shops:
            if shop["shopid"]== new_shop["shopid"]:
              new_shop_exists = True
          if not new_shop_exists:
            shops.append(new_shop)

        time.sleep(random.uniform(20, 25))
        reviews_data = get_reviews_from_shopee_api(shopid,itemid,product)
        products.append(product)
        rows.extend(reviews_data)
      else:
          print("No match found.",url)
      # wait = WebDriverWait(driver, 10)
      # wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

      # page = driver.page_source
      # soup = BeautifulSoup(page, 'html.parser')
      
      # reviews = soup.find_all("div", {"class": reviews_section_class})

      # if len(reviews)>0:
      #   product = {"url":url}

      #   product_title_element = soup.find("div", {"class": product_title_class})
      #   if (product_title_element):
      #     product_name_element = product_title_element.find("span")
      #     if (product_name_element):
      #       # product_name = product_name_element.text
      #       product["name"]=product_name_element.text

      #   for element_to_scrape in ELEMENTS_TO_SCRAPE:
      #     element = soup.find(["div","span"], {"class": element_to_scrape["class"]})
      #     if element:
      #       text=element.get_text(separator="\n")
      #       product[element_to_scrape["name"]]=text

      #   category_elements = soup.find_all("a", {"class": category_class})
      #   if len(category_elements)>0:
      #     categories_list = []
      #     for category_element in category_elements:
      #       categories_list.append(category_element.text)
      #     product["categories"] = ">".join(categories_list)
      #     product["category"] = category_elements[-1].text

      #   primary_image_element =  soup.find("div", {"class": product_primary_image_class})
      #   if primary_image_element and primary_image_element.has_attr("style"):
      #     div_style = primary_image_element['style']
      #     style = cssutils.parseStyle(div_style)
      #     image_url = style['background-image']
      #     image_url = image_url.replace('url(', '').replace(')', '')    # or regex/split/find/slice etc. 
      #     product["image_url"]=image_url       

      #   else:
      #     secondary_image_element =  soup.find("div", {"class": product_secondary_image_class})
      #     if secondary_image_element and secondary_image_element.has_attr("style"):
      #       div_style = secondary_image_element['style']
      #       style = cssutils.parseStyle(div_style)
      #       image_url = style['background-image']
      #       image_url = image_url.replace('url(', '').replace(')', '')    # or regex/split/find/slice etc.   
      #       product["image_url"]=image_url 
        


    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print('----error----')
      print(exc_type, fname, exc_tb.tb_lineno)


  # for index,link in enumerate(links):
  #   # count=index+1
  #   # if count>products_pages_to_scrape:
  #   #   break
  #   scrape_shopee_product_reviews(link)
    

  # define the output file name and field names
  products_output_file = f'shopee_products_{category}.xlsx'
  reviews_output_file = f'shopee_reviews_{category}.xlsx'
  shops_output_file = f'shopee_shops_{category}.xlsx'
  # reviews_custom_order = ["shopid","itemid","ctime","author_username","comment","rating_star","template_tags"]
  # products_custom_order = ["url","shopid","itemid","name","original_price","current_price","description","rating","image_url","items_sold"]

  try:
    # write the list of dictionaries to a excel file
    df = pd.DataFrame.from_dict(rows) 
    # df = df.reindex(columns=reviews_custom_order)
    df.to_excel(reviews_output_file, index = False, header=True)  

    products_df = pd.DataFrame.from_dict(products) 
    # Define a custom sorting key function
    # def custom_sort_key(item):
    #     try:
    #         return products_custom_order.index(item)
    #     except ValueError:
    #         return len(products_custom_order)
    # modified_products_custom_order = sorted(list(products_df.columns), key=custom_sort_key)
    # products_df = products_df.reindex(columns=modified_products_custom_order)
    products_df.to_excel(products_output_file, index = False, header=True)  

    shops_df = pd.DataFrame.from_dict(shops) 
    shops_df.to_excel(shops_output_file, index = False, header=True)  

  except Exception as e:
    print(e)

# categories = ["Food-Beverages-cat.11011871","Beauty-Personal-Care-cat.11012301","Home-Appliances-cat.11027421","Mobile-Gadgets-cat.11013350","Men's-Wear-cat.11012963","Sports-Outdoors-cat.11012018","Video-Games-cat.11013478","Hobbies-Books-cat.11011760","Women's-Bags-cat.11012592","Travel-Luggage-cat.11012566"]
# categories = ["Home-Appliances-cat.11027421"]
# "Video-Games-cat.11013478","Hobbies-Books-cat.11011760","Women's-Bags-cat.11012592","Travel-Luggage-cat.11012566"
categories=["Hobbies-Books-cat.11011760","Cameras-Drones-cat.11013548"]

# categories = ["Beauty-Personal-Care-cat.11012301"]

for category in categories:
  main(category)