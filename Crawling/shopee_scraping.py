from tkinter import W
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
import sys, os
import csv
import random
from selenium.webdriver.common.action_chains import ActionChains
import cssutils



# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

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
    author_class = "shopee-product-rating__author-name"
    time_class = "shopee-product-rating__time"
    full_star_class = "shopee-svg-icon icon-rating-solid--active icon-rating-solid"
    empty_star_class = "shopee-svg-icon icon-rating"

    primary_page_button_class ="shopee-button-solid shopee-button-solid--primary"
    next_page_button_class ="shopee-button-no-outline"
    reviews_text_class = "Rk6V+3"

    review_preset_attributes_class = "XgpZlY" #eg: Performance, Best Feature(s), Value For Money

    product_title_class = "_44qnta"
    # maybe image url, price , items sold and so on
    original_price_class = "Y3DvsN"
    discounted_price_class = "pqTWkA"
    product_description_class = "f7AU53"

    product_primary_image_class ="VWiifV qO2bZw"
    product_secondary_image_class = "A4dsoy qO2bZw"

    # filter_reviews_with_comments_button_class = "product-rating-overview__filter product-rating-overview__filter--with-comment"


    ELEMENTS_TO_SCRAPE = [{"name":"original_price", "class":original_price_class},{"name":"discounted_price", "class":discounted_price_class},{"name":"product_description", "class":product_description_class}]


    # SUBSECTION_ATTRIBUTES = ["Performance","Best Feature(s)","Value For Money"]
    is_product_scraped = False
    # reviews_count= 0 
    try:
      count=0
      while True:
        # count+=1
        # if (count>reviews_pages_to_scrape):
        #   break
        delay = random.uniform(1, 3)
        time.sleep(delay)
        # time.sleep(1)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        
        reviews = soup.find_all("div", {"class": reviews_section_class})

        if len(reviews)>0 and is_product_scraped==False:
          # product_name = ""
          # product_description = ""
          # product_original_price = ""
          # product_discounted_price = ""
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
          products.append(product)
          is_product_scraped=True

        for review in reviews:
          # row={"product_name":product_name}
          row={}

          author_element = review.find(class_=author_class)
          if (author_element):
            row["author"] = author_element.text

          time_element = review.find("div", {"class": time_class})
          if (time_element):
            row["time"] = time_element.text



          stars = len(review.find_all("svg", {"class": full_star_class}))
          row["stars"] = stars

          text_element = review.find("div", {"class": reviews_text_class})
          if (text_element):
            # find only the direct childs
            text_sub_sections = text_element.find_all(recursive=False)
            if len(text_sub_sections)>0:
              product_attributes_review_list = []
              for text_sub_section in text_sub_sections:
                hasChild = text_sub_section.find("span", {"class": review_preset_attributes_class})
                if hasChild:
                  product_attribute_text = text_sub_section.get_text(separator=" ")
                  product_attributes_review_list.append(product_attribute_text)
                  
                  # text_sub_section_elements = text_sub_section.text.split(":")
                  # # length should be 2 actually
                  # if (len(text_sub_section_elements)==2):
                  #   subsection_attribute, subsection_text = text_sub_section_elements
                  #   if subsection_attribute in SUBSECTION_ATTRIBUTES:
                  #     row[subsection_attribute]=subsection_text.strip()
                  #   else:
                  #     print("Unkown subsection attribute:",subsection_attribute)
                  # else:
                  #   print("text_sub_section_elements length less than 2.")
                else:
                  row["text"] = text_sub_section.text
              row["product_attributes_review"]="\n".join(product_attributes_review_list)
            else:
              row["text"] = text_element.text
          row["url"] = url

          rows.append(row)

        buttons_xpath = f"//button[@class='{primary_page_button_class}']/following-sibling::button[@class='{next_page_button_class}']"
        current_page_buttons =  driver.find_elements(By.XPATH, buttons_xpath)
        if len(current_page_buttons)>0:
          WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, buttons_xpath)))
          next_page_button = driver.find_element(By.XPATH, buttons_xpath)
          ActionChains(driver).move_to_element(next_page_button).click().perform()

          # current_page_button = driver.find_element(By.XPATH,f"//button[@class='{primary_page_button_class}']/following-sibling::button[@class='{next_page_button_class}']")
          # current_page_button.click()
        else:
          break

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
  custom_order = ["author", 'time', 'stars', "product_attributes_review", "text", "url"]

  try:
    # write the list of dictionaries to a CSV file
    df = pd.DataFrame.from_dict(rows) 
    df = df.reindex(columns=custom_order)
    df.to_excel(reviews_output_file, index = False, header=True)  

    products_df = pd.DataFrame.from_dict(products) 
    products_df.to_excel(products_output_file, index = False, header=True)  
    # with open(reviews_output_file, 'w', newline='', encoding="utf-8") as csvfile:
    #     writer = csv.DictWriter(csvfile, fieldnames=field_names)
    #     writer.writeheader()
    #     for data_row in rows:
    #         writer.writerow(data_row)
  except Exception as e:
    print(e)
    with open(rf'shopee_reviews_dataset_{category}.txt', 'w', encoding="utf-8") as fp:
      for row in rows:
          # write each item on a new line
          fp.write(row+"\n")
      print('Done')
    with open(rf'shopee_products_{category}.txt', 'w', encoding="utf-8") as fp:
      for product in products:
          # write each item on a new line
          fp.write(product+"\n")
      print('Done')

categories = ['laptop',"Home-Living-cat.11000001"]

for category in categories:
  main(category)
# print(rows)

# wait for the reviews section to load
# reviews_section = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CLASS_NAME, reviews_section_class))
# )

# # scroll to the bottom of the page to load more reviews
# while True:
#     last_review = driver.find_elements_by_class_name('_3Oj5_n')[-1]
#     driver.execute_script('arguments[0].scrollIntoView()', last_review)
#     try:
#         load_more_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, '_1JBBvG'))
#         )
#         load_more_button.click()
#     except:
#         break

# extract the reviews
# reviews = driver.find_elements_by_class_name(reviews_section_class)
# reviews = driver.find_elements(By.CLASS_NAME, reviews_section_class)

# for review in reviews:
  # print(review.text)
    # text_element = review.find_element(By.CLASS_NAME, "Rk6V+3")
    # if (text_element):
    #   print(text_element.text)
    # rating = review.find_element_by_class_name('_3LWZlK').get_attribute('aria-label')
    # user = review.find_element_by_class_name('_2mcZGG').text
    # date = review.find_element_by_class_name('OitLRu').text
    # print(text, rating, user, date)
    # print(text)

# close the driver
driver.quit()
