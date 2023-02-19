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
* `original_price`: The original price of the product (before any discounts).
* `current_price`: The current price of the product after any discounts if there is any.
* `description`: A text description of the product.
* `rating`: The overall rating of the product.
* `image_url`: The URL of an image that shows the product.
* `shopid`: A unique identifier for the store that sells the product.
* `itemid`: A unique identifier for the product being sold.

## shopee_product_links.txt
This dataset contains URLs of the products.
