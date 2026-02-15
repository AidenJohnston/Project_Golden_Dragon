#Getting the final product list after clearing out all the invalid items
import bazaarFunctions as bf
import pandas as pd
import numpy as np
import requests


bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"
items = bf.get_bazaar_list(bf.get_bazaar_data(bazaar_url))

finalProducts = []

for item in items:
    if (((item.get("sellMovingWeek") != 0) | (item.get("buyMovingWeek") != 0))):
        print(item.get("productId"))
        print(item.get("sellPrice"))
        print(item.get("sellMovingWeek"))
        print(item.get("buyPrice"))
        print(item.get("buyMovingWeek"))
        finalProducts.append(item.get("productId"))

with open('productList.txt', 'w') as file:
    for product in finalProducts:
        file.write(str(product) + '\n')

