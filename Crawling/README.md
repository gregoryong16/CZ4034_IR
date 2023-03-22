# About Dataset
The data folder contains the following files:
* `shopee_reviews.xlsx`
* `shopee_products.xlsx`
* `shopee_product_links.txt`

## shopee_reviews.xlsx
This dataset contains reviews for products sold on Shopee. The dataset includes the following columns:

* `shopid`: A unique identifier for the store where the product was purchased.
* `itemid`: A unique identifier for the product being reviewed.
* `ctime`: The unix timestamp that the review was submitted.
* `author_username`: The username of the customer who submitted the review.
* `comment`: The text of the review.
* `rating_star`: The number of stars (out of 5) given in the review.
* `template_tags`: A list of tags assigned to the review by the customer to describe the product. eg: ["Performance", "Product Quality"] 

Note: This dataset only includes reviews from products listed on `shopee_products.xlsx`. Number of the products is 40 currently, will continue to scrape more.

## shopee_products.xlsx
This dataset contains information on products sold on Shopee. The dataset includes the following columns:

* `url`: The URL of the product page on the Shopee platform.
* `name`: The name of the product.
* `price_min`: The minimum price of the product.
* `price_max`: The maximum price of the product.
* `price_middle`: The middle price of the product.
* `description`: A text description of the product.
* `rating`: The overall rating of the product.
* `image_url`: The URL of an image that shows the product.
* `shopid`: A unique identifier for the store that sells the product.
* `itemid`: A unique identifier for the product being sold.
* `items_sold`: The number of units of the product that have been sold.
* `category`: The category to which the product belongs.
* `rating_total`: The total number of customer reviews for the product..

## shopee_shops.xlsx
This dataset contains information on shops on Shopee. The dataset includes the following columns:

* `shopid`: A unique identifier for the shop.
* `userid`: The user ID of the shop owner.
* `place`: The address of the shop.
* `shop_location`: The location of the shop.
* `item_count`: The total number of items listed for sale in the shop.
* `rating_star`: The average star rating for the shop, based on customer reviews.
* `response_rate`: The percentage of customer inquiries that the shop owner responds to.
* `name`: The name of the shop.
* `response_time`: The average time (in seconds maybe) it takes for the shop owner to respond to customer inquiries.
* `follower_count`: The total number of customers who have added the shop to their list of favorites.
* `rating_bad`: The number of customer reviews with a "bad" rating (1 or 2 stars).
* `rating_good`: The number of customer reviews with a "good" rating (4 or 5 stars).
* `rating_normal`: The number of customer reviews with a "normal" rating (3 stars).
* `username`: The username of the shop owner.

## shopee_review_product_shop_combined.xlsx
This joined version of the datasets.

## shopee_product_links.txt
This dataset contains URLs of the products.
