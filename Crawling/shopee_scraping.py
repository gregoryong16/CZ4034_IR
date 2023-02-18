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
def get_reviews_from_shopee_api(shopid,itemid):
  reviews = []
  try:
    offset=0
    while True:
      # filter the reviews with comments
      url = f'https://shopee.sg/api/v2/item/get_ratings?filter=1&flag=1&itemid={itemid}&limit=50&offset={offset}&shopid={shopid}&type=0'
      # Make a request to the API
      response = requests.get(url)
      # Load the response JSON into a Python dictionary
      data = json.loads(response.text)
      # Extract the data you need from the dictionary
      results = data['data']['ratings']
      if (results==None):
        break
      # keys to select
      selected_keys = ["shopid","itemid","ctime","author_username","comment","rating_star","template_tags"]
      # create a new list of dictionaries with only selected keys
      new_results = [{key: d[key] for key in selected_keys} for d in results]
      reviews.extend(new_results)
      offset+=len(results)


  except Exception as e:
    print(e)

  return reviews

def main(category):
  # set up the driver (make sure to download the appropriate driver for your browser)
  driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe')
  rows = []
  products = []

  # reviews_pages_to_scrape = 2
  products_pages_to_scrape = 20


  my_file = open(f"shopee_product_links_{category}.txt", "r" , encoding="utf-8" )
  data = my_file.read()
  links = data.split("\n")
  my_file.close()


  def scrape_shopee_product_reviews(url):
    print(url)
    # navigate to the Shopee product page
    driver.get(url)

    reviews_section_class = "shopee-product-rating__main"

    product_title_class = "_44qnta"
    # maybe image url, price , items sold and so on
    original_price_class = "Y3DvsN"
    discounted_price_class = "pqTWkA"
    product_description_class = "f7AU53"

    product_primary_image_class ="VWiifV qO2bZw"
    product_secondary_image_class = "A4dsoy qO2bZw"
    rating_class = "product-rating-overview__rating-score"

    ELEMENTS_TO_SCRAPE = [{"name":"original_price", "class":original_price_class},{"name":"discounted_price", "class":discounted_price_class},{"name":"description", "class":product_description_class},{"name":"rating", "class":rating_class}]


    try:
      count=0
      delay = random.uniform(1, 3)
      time.sleep(delay)
      wait = WebDriverWait(driver, 10)
      wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

      page = driver.page_source
      soup = BeautifulSoup(page, 'html.parser')
      
      reviews = soup.find_all("div", {"class": reviews_section_class})

      if len(reviews)>0:
        product = {"url":url}

        product_title_element = soup.find("div", {"class": product_title_class})
        if (product_title_element):
          product_name_element = product_title_element.find("span")
          if (product_name_element):
            # product_name = product_name_element.text
            product["name"]=product_name_element.text

        for element_to_scrape in ELEMENTS_TO_SCRAPE:
          element = soup.find("div", {"class": element_to_scrape["class"]})
          if element:
            text=element.get_text(separator="\n")
            product[element_to_scrape["name"]]=text

        primary_image_element =  soup.find("div", {"class": product_primary_image_class})
        if primary_image_element and primary_image_element.has_attr("style"):
          div_style = primary_image_element['style']
          style = cssutils.parseStyle(div_style)
          image_url = style['background-image']
          image_url = image_url.replace('url(', '').replace(')', '')    # or regex/split/find/slice etc. 
          product["image_url"]=image_url       

        else:
          secondary_image_element =  soup.find("div", {"class": product_secondary_image_class})
          if secondary_image_element and secondary_image_element.has_attr("style"):
            div_style = secondary_image_element['style']
            style = cssutils.parseStyle(div_style)
            image_url = style['background-image']
            image_url = image_url.replace('url(', '').replace(')', '')    # or regex/split/find/slice etc.   
            product["image_url"]=image_url 
        
        match = re.search(r"i\.(\d+)\.(\d+)$", url)

        if match:
          shopid = match.group(1)
          itemid = match.group(2)

          product["shopid"] = shopid
          product["itemid"] = itemid
          products.append(product)

          time.sleep(random.uniform(1, 2))
          reviews = get_reviews_from_shopee_api(shopid,itemid)
          rows.extend(reviews)
        else:
            print("No match found.",url)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print('----error----')
      print(exc_type, fname, exc_tb.tb_lineno)


  for index,link in enumerate(links):
    count=index+1
    if count>products_pages_to_scrape:
      break
    scrape_shopee_product_reviews(link)
    

  # define the output file name and field names
  products_output_file = f'shopee_products_{category}.xlsx'
  reviews_output_file = f'shopee_reviews_dataset_{category}.xlsx'
  custom_order = ["shopid","itemid","ctime","author_username","comment","rating_star","template_tags"]

  try:
    # write the list of dictionaries to a excel file
    df = pd.DataFrame.from_dict(rows) 
    df = df.reindex(columns=custom_order)
    df.to_excel(reviews_output_file, index = False, header=True)  

    products_df = pd.DataFrame.from_dict(products) 
    products_df.to_excel(products_output_file, index = False, header=True)  

  except Exception as e:
    print(e)
    with open(rf'shopee_reviews_dataset_{category}.txt', 'w', encoding="utf-8") as fp:
      for row in rows:
          fp.write(row+"\n")
      print('Done')
    
    with open(rf'shopee_products_{category}.txt', 'w', encoding="utf-8") as fp:
      for product in products:
          fp.write(product+"\n")
      print('Done')

categories = ['Computers-Peripherals-cat.11013247',"Home-Living-cat.11000001"]

for category in categories:
  main(category)