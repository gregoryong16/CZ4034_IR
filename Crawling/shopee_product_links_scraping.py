from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import pandas as pd
import sys, os
from urllib.parse import urljoin, urlparse


# set up the driver (make sure to download the appropriate driver for your browser)
driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe')

keyword = "laptop"
# navigate to the Shopee product page
# url =f'https://shopee.sg/search?keyword={keyword}'
categories = ["Computers-Peripherals-cat.11013247","Home-Living-cat.11000001"]
category = "Computers-Peripherals-cat.11013247"
url = f"https://shopee.sg/{category}"
driver.get(url)

item_class = "shopee-search-item-result__item"
primary_page_button_class ="shopee-button-solid shopee-button-solid--primary"
next_page_button_class ="shopee-button-no-outline"

links = []
try:
  pages_to_fectch = 2
  for i in range(pages_to_fectch):
    time.sleep(2)
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # get the height of the entire webpage
    page_height = driver.execute_script("return document.body.scrollHeight")

    # set the scroll speed and duration
    scroll_speed = 400
    scroll_duration = 0.2

    # scroll to the bottom of the page slowly
    for i in range(0, page_height, scroll_speed):
        driver.execute_script("window.scrollTo(0, {});".format(i))
        time.sleep(scroll_duration)

    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    

    items = soup.find_all("div", {"class": item_class})
    print(len(items))
    for item in items:
      link_element = item.find("a")
      if (link_element):
        link=f"https://shopee.sg{link_element['href']}"
        # remove query parameters
        link = urljoin(link, urlparse(link).path) 
        links.append(link)
    
    current_page_buttons =  driver.find_elements(By.XPATH,f"//button[@class='{primary_page_button_class}']/following-sibling::button[@class='{next_page_button_class}']")
    if len(current_page_buttons)>0:
      WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"//button[@class='{primary_page_button_class}']/following-sibling::button[@class='{next_page_button_class}']"))).click()
    else:
      break

except Exception as e:
  exc_type, exc_obj, exc_tb = sys.exc_info()
  fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
  print(exc_type, fname, exc_tb.tb_lineno)


# open file in write mode
with open(rf'shopee_product_links_{category}.txt', 'w', encoding="utf-8") as fp:
    for link in links:
        # write each item on a new line
        fp.write(link+"\n")
    print('Done')

# close the driver
driver.quit()
