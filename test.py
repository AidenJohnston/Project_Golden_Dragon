import bazaarFunctions as bf
import requests

bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"

items = bf.get_bazaar_list(bf.get_bazaar_data(bazaar_url))

bf.bidAskSpread_plot(items)

### This one was for plotting the sellMovingWeek of the top 20 items
#sorted = bf.highest_sellMovingWeek(items)
#df = pd.DataFrame(sorted, columns = ["productId", "sellPrice", "sellMovingWeek", "buyPrice", "buyMovingWeek"])
#df.plot(kind='scatter', x='productId', y='sellMovingWeek')
#plt.show()