import requests
import json
from pprint import pprint

# simple get function I'm stealing from 0x26e
def get_info(call):
    r = requests.get(call)
    return r.json()

# returns the entirety of the bazaar lmao
def get_bazaar_data():
    return get_info(bazaar_url)


# total value of all buy orders in the bazaar
def get_bazaar_buy_order_value(bazaar_data):
    sum_coins = 0

    #looping for every item in the bazaar
    for item_name, item_data in bazaar_data.get("products", {}).items():
        item_sum_coins = 0
        price_increase_threshold = 1.2 #20% increase threshold

        #for every buy order
        for idx, buy_order in enumerate(item_data.get("buy_summary", [])):
            #if it's the best price
            if (idx == 0):
                item_expected_value = buy_order.get("pricePerUnit", 0)
                item_sum_coins += buy_order.get("amount", 0) * buy_order.get("pricePerUnit", 0)
            # if it's not the best price, check to see if it's reasonable
            else:
                if (buy_order.get("pricePerUnit", 0) < (item_expected_value * price_increase_threshold)):
                    item_sum_coins += buy_order.get("amount", 0) * buy_order.get("pricePerUnit", 0)
        print(f"{item_name} | {round(item_sum_coins)}")
        sum_coins += item_sum_coins

    return sum_coins


# going through and getting only the values that I want for every product
def get_bazaar_list(bazaar_data):
    all_items = [] #initializing an empty list
    for item_name, item_data in bazaar_data.get("products", {}).items(): #looping through every product
        stats = item_data.get("quick_status", {}) #assigning the quick_status information to another variable
        item_info = {
            "productId": stats.get("productId"),
            "sellPrice": stats.get("sellPrice"),
            "sellMovingWeek": stats.get("sellMovingWeek"),
            "buyPrice": stats.get("buyPrice"),
            "buyMovingWeek": stats.get("buyMovingWeek")
        } #yoinking the information that we want out of quick_status
        all_items.append(item_info) #adding that set to the list

    return all_items #return the list of every set

def highest_sellMovingWeek(all_items):
    sorted_list = sorted(
        all_items,
        key=lambda x: x["sellMovingWeek"],
        reverse=True
    )
    return sorted_list[:20]


bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"

#code
# pprint(get_bazaar_buy_order_value(get_bazaar_data()))

items = get_bazaar_list(get_bazaar_data())
most_volatile = highest_sellMovingWeek(items)
for item in most_volatile:
    print(f"""Item: {item["productId"]} 
      SellMovingWeek: {item["sellMovingWeek"]} 
      BuyMovingWeek: {item["buyMovingWeek"]} 
      BuyPrice: {item["buyPrice"]} 
      SellPrice: {item["sellPrice"]}""")
    #apparently you need to use triple quotes to use multiple lines, that's gay
