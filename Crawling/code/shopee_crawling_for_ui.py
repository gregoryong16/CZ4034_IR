import re
import requests
import json
import pandas as pd

class ShopeeCrawler:
    def __init__(self):
        pass
    
    def get_item_from_shopee_api(self,shopid,itemid):
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

    def get_shop_info_from_shopee_api(self,shopid):
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

        return shop_info
      
      except Exception as e:
        print(e)

    def get_reviews_from_shopee_api(self,shopid,itemid,product):
      
      reviews = []
      try:
        offset=0
        ratings_number_scraped = False
        while True:
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

          # create a new list of dictionaries with only selected keys
          new_results = [{key: shopid if key == 'shopid' else itemid if key == 'itemid' else d[key] for key in selected_keys} for d in results]

          # drop rows with no comments
          filtered_new_results = [d for d in new_results if d["comment"] != None and d["comment"].strip() != ""  ]
          if (len(new_results)==0):
            print('--- reviews results length 0---',url)
            break
          reviews.extend(filtered_new_results)
          offset+=len(new_results)
          # set reviews limit to 50
          if (len(reviews)>=50):
            break

      except Exception as e:
        print(e)

      return reviews

    def get_modified_product_shop_reviews(self,product,shop,reviews):
      # filter the product with keys
      filtered_product = product.copy()
      filtered_product['price_middle'] = (filtered_product['price_min'] + filtered_product['price_max']) / 2/100000
      filtered_product['price_middle'] = round(filtered_product['price_middle'],2)
      filtered_product['price_min'] = round((filtered_product['price_min']/100000),2)
      filtered_product['price_max'] = round((filtered_product['price_max']/100000),2)

      filtered_product['image_url'] = 'https://cf.shopee.sg/file/' + filtered_product['image']

      filtered_product['rating']=round(filtered_product['item_rating']['rating_star'],2)
      filtered_product['category']=filtered_product['categories'][-1]['display_name']

      filtered_product['items_sold'] = filtered_product.pop('historical_sold')
      selected_keys = ['url',
      'shopid',
      'itemid',
      'name',
      'price_min',
      'price_max',
          'price_middle',
      'description',
      'rating',
      'image_url',
      'items_sold',
      'category',
      'rating_total']

      filtered_product = {k: v for k, v in filtered_product.items() if k in selected_keys}

      # filter the shop with keys
      filtered_shop = shop.copy()
      filtered_shop['username']=filtered_shop['account']['username']
      if filtered_shop['shop_location'] is None or filtered_shop['shop_location']=="":
          filtered_shop['shop_location']= "Local"
      if filtered_shop['place'] is None or filtered_shop['place']=="":
          filtered_shop['place']= "Overseas"
      filtered_shop['rating_star'] = round(filtered_shop['rating_star'],2)
      selected_keys = ['shopid',
      'userid',
      'place',
      'shop_location',
      'item_count',
      'rating_star',
      'response_rate',
      'name',
      'response_time',
      'follower_count',
      'rating_bad',
      'rating_good',
      'rating_normal',
      'username']

      filtered_shop = {k: v for k, v in filtered_shop.items() if k in selected_keys}

      # Dropping duplicates
      key_set = set()
      new_reviews = []

      for d in reviews:
          key = (d['shopid'], d['itemid'], d['author_username'], d['comment'])
          if key not in key_set:
              key_set.add(key)
              new_reviews.append(d)

      # Adding the prefix to the keys
      new_product = {k if k in ('shopid', 'itemid') else 'product.' + k: v for k, v in filtered_product.items()}
      new_shop = {k if k in ('shopid', 'itemid') else 'shop.' + k: v for k, v in filtered_shop.items()}

      # Joining the list of dictionaries with the dictionary
      for d in new_reviews:
          for key in new_product.keys():
              if int(d.get('shopid')) == int(new_product.get('shopid')) and int(d.get('itemid')) == int(new_product.get('itemid')):
                  d.update(new_product)

      for d in new_reviews:
          for key in new_shop.keys():
              if int(d.get('shopid')) == int(new_shop.get('shopid')):
                  d.update(new_shop)
                  
                  
      filtered_product['shop.shop_location'] = filtered_shop['shop_location']
      filtered_product['shop.name'] = filtered_shop['name']  

      return filtered_product,filtered_shop,new_reviews      

    def get_shopee_data(self,url):
      output_reviews = []
      output_product = {}
      output_shop = {}

      try:
        match = re.search(r"i\.(\d+)\.(\d+)$", url)

        if match:
          shopid = match.group(1)
          itemid = match.group(2)

          product = self.get_item_from_shopee_api(shopid,itemid)
          product["url"] = url
          shop = self.get_shop_info_from_shopee_api(shopid)
          reviews = self.get_reviews_from_shopee_api(shopid,itemid,product)

          output_product,output_shop,output_reviews = self.get_modified_product_shop_reviews(product,shop,reviews)
        else:
            print("No match found.",url)

      except Exception as e:
        print(e)
      
      return output_product,output_shop,output_reviews
