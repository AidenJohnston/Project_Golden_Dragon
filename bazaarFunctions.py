import requests
import json
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# JSON Get function (stolen from 0x26e)
def get_info(call):
    r = requests.get(call)
    return r.json()

# returns the entirety of the bazaar
def get_bazaar_data(bazaar_url):
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

# sorts by items with highest instant sell and then returns the top 20
def highest_sellMovingWeek(all_items):
    sorted_list = sorted(
        all_items,
        key=lambda x: x["sellMovingWeek"],
        reverse=True
    )
    return sorted_list[:20]

#coflnet 1 week price history given item_tag
def get_bazaar_history(item_tag, days=7):

    """Get bazaar price history for the last N days"""
    end = datetime.now()
    start = end - timedelta(days=days)
    
    url = f"https://sky.coflnet.com/api/bazaar/{item_tag}/history"
    params = {
        "start": start.isoformat() + "Z",
        "end": end.isoformat() + "Z"
    }
    
    response = requests.get(url, params=params)
    return response.json()

#plots the bid/ask spread of the top 5 most instasold items
def bidAskSpread_plot(items):
    sorted = highest_sellMovingWeek(items)
    first_five = sorted[:5]

    for index in first_five:
        
        item_id = index.get('productId')
        history = get_bazaar_history(item_id)
        previous_bidAsk = 0
        information_week = []

        for entry in history:

            timestamp = entry.get('timestamp', 'Unknown Time')

            buy_price = entry.get('buy', 0)
            sell_price = entry.get('sell', 0)

            print(f"{timestamp}: Buy {buy_price}, Sell {sell_price}")

            if (buy_price != 0):
                bidAsk_spread = ((buy_price - sell_price)/(buy_price)) * 100
                previous_bidAsk = bidAsk_spread
            else:
                bidAsk_spread = previous_bidAsk

            information_week.insert(0, [timestamp, bidAsk_spread])

        if information_week:
            df = pd.DataFrame(information_week, columns=["timestamp", "bidAsk_spread"])
            df["timestamp"] = pd.to_datetime(df["timestamp"]) #turning this gay bullshit into a pandas datetime object for easier formatting
            plt.plot(df["timestamp"], df["bidAsk_spread"], label=item_id)


    plt.title("Bid/Ask Spread Comparison (Top 5 most Instasold Items)")
    plt.xlabel("Timestamp")
    plt.ylabel("Spread (%)")

    my_format = mdates.DateFormatter('%m/%d-%H:%M')
    plt.gca().xaxis.set_major_formatter(my_format)

    plt.legend(loc='upper left', fontsize='small', ncol=2)

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()