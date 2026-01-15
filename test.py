import matplotlib.pyplot as plt
import pandas as pd
import bazaarFunctions as bf
import requests
import matplotlib.dates as mdates

bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"

items = bf.get_bazaar_list(bf.get_bazaar_data(bazaar_url))

# Usage
sorted = bf.highest_sellMovingWeek(items)
first_five = sorted[:5]

for index in first_five:
    
    item_id = index.get('productId')
    history = bf.get_bazaar_history(item_id)
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


### This one was for plotting the sellMovingWeek of the top 20 items
#sorted = bf.highest_sellMovingWeek(items)
#df = pd.DataFrame(sorted, columns = ["productId", "sellPrice", "sellMovingWeek", "buyPrice", "buyMovingWeek"])
#df.plot(kind='scatter', x='productId', y='sellMovingWeek')
#plt.show()