import bazaarFunctions as bf
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"

items = bf.get_bazaar_list(bf.get_bazaar_data(bazaar_url))

item_tag = "STOCK_OF_STONKS"
history = bf.get_bazaar_history(item_tag, days=90)
information = []
for entry in history:
    timestamp = entry.get("timestamp", "Unknown Time")
    buy_price = entry.get('buy', 0)
    sell_price = entry.get('sell', 0)
    mid_price = (buy_price + sell_price) / 2
    information.insert(0, [timestamp, mid_price])

if information:
    df = pd.DataFrame(information, columns=["timestamp", "mid_price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"]) #turning this gay bullshit into a pandas datetime object for easier formatting
    plt.plot(df["timestamp"], df["mid_price"], label=item_tag)

plt.title("Stock of Stonks Mid-Price Over the last 90 Days")
plt.xlabel("Timestamp")
plt.ylabel("Mid-Price")

my_format = mdates.DateFormatter('%m/%d-%H:%M')
plt.gca().xaxis.set_major_formatter(my_format)


plt.xticks(rotation=45)
plt.tight_layout()

plt.show()





### another function for plotting the bid/ask spread of the top 5 most instasold items
#bf.bidAskSpread_plot(items)

### This one was for plotting the sellMovingWeek of the top 20 items
#sorted = bf.highest_sellMovingWeek(items)
#df = pd.DataFrame(sorted, columns = ["productId", "sellPrice", "sellMovingWeek", "buyPrice", "buyMovingWeek"])
#df.plot(kind='scatter', x='productId', y='sellMovingWeek')
#plt.show()