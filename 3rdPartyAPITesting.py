#time to scrape the forums for API's that people stopped maintaining


#found the coflnet one (I stole this code from their docs)
import requests
from datetime import datetime, timedelta

def get_bazaar_history(item_tag, days=7):
    """Get bazaar price history for the last N days"""
    end = datetime.utcnow()
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
for entry in history:
    print(f"{entry['timestamp']}: Buy {entry['buy']}, Sell {entry['sell']}")