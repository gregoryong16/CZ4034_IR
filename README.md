# A Django webapp with elasticsearch backend(NoSQL)

## Steps to get the app running on your local machine

### 1. Install files in requirements.txt (make sure you're in the CZ4034 folder) by entering the command

```
pip install -r requirements.txt
```

### 2. Install the elasticsearch(required for searching) file in **Indexing** directory

<br/>

Head to this [link](https://www.elastic.co/downloads/past-releases/elasticsearch-7-14-0) and download the zipfile by clicking on **WINDOWS or MACOS** depending on your OS.

<br/>

### 3. Run the elasticsearch backend by changing directory to Indexing\elasticsearch-7.14.0\bin then run the elasticsearch backend by executing the command:

```
cd Indexing\elasticsearch-7.14.0\bin
elasticsearch.bat
```

now head to [localhost:9200](http://localhost:9200)

### 4. Install the chromedriver file(required for crawling) file in **Indexing** directory

<br/>

Head to this [link](https://chromedriver.chromium.org/downloads) and download chromdriver according to your OS.

<br/>

### 4. Open a new terminal and package model changes into individual migration files - analogous to commits

```
cd Indexing
python manage.py makemigrations --name initial_setup
```

### 5. Apply the changes to the database

```
python manage.py migrate
```

### 6. Populate the database by running the load_products.py file.

```
cd indexing_project
python load_products.py
```

### 7. Build index

```
cd ..
python manage.py search_index --rebuild
```

### 8. Run django app server

```
python manage.py runserver
```

now head to [localhost:8000](http://localhost:8000)

<br/>

## You're Done with the set up, congrats! Now you're able to search/crawl for products on our application!

<br/>

# For Searching

## Input any **_product name_** you want to search for! Like keyboard, laptop, mouse etc.

<br/>

# For crawling

## Input any **_product category url_** from **_Shopee_** you want to crawl, for example, something like "[https://shopee.sg/Cameras-Drones-cat.11013548](https://shopee.sg/Cameras-Drones-cat.11013548)"
