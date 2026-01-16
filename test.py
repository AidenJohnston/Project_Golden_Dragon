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


#this looks like AIDS, I never wish a code review like this for my worst enemy
import numpy as np
df["log_return"] = np.log(df["mid_price"]).diff() # Log returns
rf_annual = 0.0419 #4.19% risk-free-return according to the US Treasury
periods_per_year = 365 * 12  # periods per year (12 entries per day, 365 days)
rf_period = (1 + rf_annual) ** (1 / periods_per_year) - 1 # Convert annual rf -> per-period rf (compounding-consistent)
df["excess_return"] = df["log_return"] - rf_period # Excess returns
excess = df["excess_return"].dropna() # Drop the first NaN
mean_excess = excess.mean()
std_excess = excess.std(ddof=1)
sharpe_period = mean_excess / std_excess
sharpe_annual = sharpe_period * np.sqrt(periods_per_year)
print("Mean excess return (per period):", mean_excess)
print("Std dev excess return (per period):", std_excess)
print("Sharpe (per period):", sharpe_period)
print("Sharpe (annualized):", sharpe_annual)

### another function for plotting the bid/ask spread of the top 5 most instasold items
#bf.bidAskSpread_plot(items)

### This one was for plotting the sellMovingWeek of the top 20 items
#sorted = bf.highest_sellMovingWeek(items)
#df = pd.DataFrame(sorted, columns = ["productId", "sellPrice", "sellMovingWeek", "buyPrice", "buyMovingWeek"])
#df.plot(kind='scatter', x='productId', y='sellMovingWeek')
#plt.show()