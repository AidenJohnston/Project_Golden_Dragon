import numpy as np
import requests

#Net Spread
def netSpread(sell, buy):
    return ((sell-buy) - (sell * 0.01125))

#Spread Percentage
def spreadPercentage(sell, buy):
    return (((sell-buy)/(buy)) * 100)

#Profit Margin
def profitMargin(sell, buy):
    return (((sell*0.98875) - buy)/(buy))

#Transaction Velocity (Items/minute)
def transactionVelocity(sellMovingWeek):
    return (sellMovingWeek/10080)

#Turnover Time (Minutes)
def turnoverTime(sellMovingWeek):
    return (1/transactionVelocity(sellMovingWeek))

#Buy/Sell Volume Ratio
def bsVolumeRatio(buyMovingWeek, sellMovingWeek):
    return (buyMovingWeek/sellMovingWeek)

#Price History in the Last 24 Hours
def getPriceHistory(productId):
    request_URL = "https://sky.coflnet.com/api/bazaar/{productId}/history/day"
    history = requests.get(request_URL)
    priceHistory = []
    for entry in history:
        priceHistory.append(entry['buy'])
    return priceHistory

#Rolling Volatility (Last 24 Hours)
def rollingVolatility(productId):
    return np.std(getPriceHistory(productId))

#Coefficient of Variation
def variationCoefficient(productId):
    priceHistory = getPriceHistory(productId)
    rollingMeanPrice = np.mean(priceHistory)
    rollingVolatility = rollingVolatility(priceHistory)
    return ((rollingVolatility)/(rollingMeanPrice))

#Z-Score
def z_score():
    return #i'm gonna finish this one later too

#Price Momentum
def priceMomentum(productId):
    request_URL = "https://sky.coflnet.com/api/bazaar/{productId}/snapshot"
    
    timestamp = datetime.now() - timedelta(hours=6)
    response = requests.get(request_URL, params=timestamp)
    price3SnapshotsAgo = response['buy']

    timestamp = datetime.now()
    response = requests.get(request_URL, params=timestamp)
    currentPrice = response['buy']

    return ((currentPrice/price3SnapshotsAgo) - 1)

#Simple Moving Average Crossover
def SMA_Crossover(productId):
    request_URL = f"https://sky.coflnet.com/api/bazaar/{productId}/history"
    
    end = datetime.now()
    start = end - timedelta(hours=6)
    params = {
        "start": start.isoformat() + "Z",
        "end": end.isoformat() + "Z"
    }
    history = requests.get(request_URL, params=params)
    priceHistory = []
    for entry in history:
        priceHistory.append(entry['buy'])
    ThreeSSMean = np.mean(priceHistory)
    
    end = datetime.now()
    start = end - timedelta(hours=24)
    params = {
        "start": start.isoformat() + "Z",
        "end": end.isoformat() + "Z"
    }
    history = requests.get(request_URL, params=params)
    priceHistory = []
    for entry in history:
        priceHistory.append(entry['buy'])  
    TwelveSSMean = np.mean(priceHistory)

    return (ThreeSSMean/TwelveSSMean)

#Spread Stability (Last 12 hours)
def spreadStability(productId):
    request_URL = f"https://sky.coflnet.com/api/bazaar/{productId}/history"
    
    end = datetime.now()
    start = end - timedelta(hours=12)
    params = {
        "start": start.isoformat() + "Z",
        "end": end.isoformat() + "Z"
    }
    history = requests.get(request_URL, params=params)
    netSpread = []
    for entry in history:
        netSpread.append(netSpread(entry['sell'], entry['buy']))
    
    return np.std(netSpread)

#Market Depth Impact
def marketDepthImpact(productId):
    return #i'll finish this one later

