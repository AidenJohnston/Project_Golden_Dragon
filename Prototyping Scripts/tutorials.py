import bazaarFunctions as bf

bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"

items = bf.get_bazaar_list(bf.get_bazaar_data(bazaar_url))
most_volatile = bf.highest_sellMovingWeek(items)
index = 1
for item in most_volatile:
    print(f"""Item {index}: {item["productId"]} 
      SellMovingWeek: {item["sellMovingWeek"]} 
      BuyMovingWeek: {item["buyMovingWeek"]} 
      BuyPrice: {item["buyPrice"]} 
      SellPrice: {item["sellPrice"]}""")
    index += 1
    #apparently you need to use triple quotes to use multiple lines, that's gay

#so now I kinda want to graph Hard Stone and the Sharpe Ratio for that
