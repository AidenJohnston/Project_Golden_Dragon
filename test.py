import matplotlib.pyplot as plt
import pandas as pd
import bazaarFunctions as bf
from datetime import datetime, timedelta
import requests

bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"

items = bf.get_bazaar_list(bf.get_bazaar_data(bazaar_url))

### This one was for plotting the sellMovingWeek of the top 20 items
#sorted = bf.highest_sellMovingWeek(items)
#df = pd.DataFrame(sorted, columns = ["productId", "sellPrice", "sellMovingWeek", "buyPrice", "buyMovingWeek"])
#df.plot(kind='scatter', x='productId', y='sellMovingWeek')
#plt.show()



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

# Usage
item = input("Enter ProductID: ")
history = get_bazaar_history(item)
information_week = []
for entry in history:
    timestamp = entry.get('timestamp', 'Unknown Time')
    buy_price = entry.get('buy', 0)
    sell_price = entry.get('sell', 0)
    print(f"{timestamp}: Buy {buy_price}, Sell {sell_price}")
    bidAsk_spread = ((buy_price - sell_price)/(buy_price)) * 100
    information_week.append([timestamp, bidAsk_spread])

df = pd.DataFrame(information_week, columns=["timestamp", "bidAsk_spread"])
df.plot(kind="line", x="timestamp", y="bidAsk_spread")
plt.show()