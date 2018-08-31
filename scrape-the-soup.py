#
#
# Inspired by the koki25ando's "Kyoto Restaurant Reviews Dataset" on Kaggle which is created in R.
# This first commit focuses on the data categories "Restaurant Name, "Station", "Category", "Rating" and "Price".
# Further features can be added with the next commit.
#
#
# Useful links:
# ttps://www.kaggle.com/koki25ando/the-best-izakaya-restaurant-in-kyoto
# https://github.com/koki25ando/Kyoto-Food-Restaurant-Data-Scraping/blob/master/kyoto.R
# https://medium.freecodecamp.org/how-to-scrape-websites-with-python-and-beautifulsoup-5946935d93fe
#
#
# Scraping rules:
# 1. You should check a website’s Terms and Conditions before you scrape it. Be careful to read the statements about legal use of data.
# Usually, the data you scrape should not be used for commercial purposes.
# 2. Do not request data from the website too aggressively with your program (also known as spamming), as this may break the website.
# Make sure your program behaves in a reasonable manner (i.e. acts like a human). One request for one webpage per second is good practice.
# 3. The layout of a website may change from time to time, so make sure to revisit the site and rewrite your code as needed
#
#

# import libraries
import urllib3
import certifi
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from time import sleep
from random import randint



# query the website and return the html to the variable "page"
def get_page(url):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url, headers = {"Accept-Language": "en-US, en;q=0.5"})
    soup = BeautifulSoup(response.data.decode('utf-8'))
    return soup



# specifying the url
url = "https://tabelog.com/en/kyoto/rstLst/"
url_test = "https://tabelog.com/en/kyoto/rstLst/1"

# https://www.dataquest.io/blog/web-scraping-beautifulsoup/


# Creation of lists to store scraped data
names = []
stations = []
categories = []
prices = []
ratings = []


# Looping over all pages
for i in range(1,61):

    # Setting up the proper url
    current_url = url + str(i)

    # Progress control
    print(current_url)


    # Setting a randomized sleep timer to mimic human behaviour
    sleep(randint(2, 6))

    # Getting the soup
    soup = get_page(url)

    # Getting up to 20 elements of the page as a list
    restaurant_containers = soup.find_all("li", class_="list-rst js-list-item")
    individual_container_length = len(restaurant_containers)
    current_restaurant = restaurant_containers[2]


    # Extract data from all the individual containers
    for i in range(0, individual_container_length):

        current_restaurant = restaurant_containers[i]

        rating = current_restaurant.find("b", class_="c-rating__val").text

        if rating != "-":

            # Rating
            ratings.append(float(rating))

            # Getting the name
            name = current_restaurant.a.text
            names.append(name)

            # Getting the (nearest) station
            station = current_restaurant.ul.li.text[15:-12]
            stations.append(station)

            # Getting the category
            category = current_restaurant.find("li", class_="list-rst__catg").text
            categories.append(category)

            # Price range
            price = current_restaurant.find("span", class_="c-rating__val").text
            prices.append(price)

            # TODO: extension for Latitude, Longitude etc.



restaurant_df = pd.DataFrame({"RestaurantName" : names, "Station" : stations, "Categories" : categories, "PriceRange" : prices, "Ratings" : ratings})



restaurant_df.to_csv("restaurantData_V1.csv")