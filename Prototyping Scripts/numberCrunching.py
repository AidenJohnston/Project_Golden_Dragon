import numpy as np
import json
import requests
from datetime import datetime, timedelta

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
    request_URL = f"https://sky.coflnet.com/api/bazaar/{productId}/history/day"
    history = (requests.get(request_URL)).json()
    priceHistory = []
    for entry in history:
        priceHistory.append(entry.get('buy'))
    return priceHistory

#Rolling Volatility (Last 24 Hours)
def rollingVolatility(productId):
    return np.std(getPriceHistory(productId))

#Coefficient of Variation
def variationCoefficient(productId):
    priceHistory = getPriceHistory(productId)
    rollingMeanPrice = np.mean(priceHistory)
    rollingVolatility = np.std(priceHistory)
    return ((rollingVolatility)/(rollingMeanPrice))

#Z-Score
def z_score(productId):
    #api stuff to get current price lmao
    request_URL = f"https://sky.coflnet.com/api/bazaar/{productId}/snapshot"
    timestamp = datetime.now().isoformat() + "Z"
    response = (requests.get(request_URL, params=timestamp)).json()

    currentPrice = response.get('buyPrice')
    priceHistory = getPriceHistory(productId) #so glad I already made this function
    average = np.mean(priceHistory)
    stDev = np.std(priceHistory)
    z_score = (currentPrice - average)/stDev
    return z_score

#Price Momentum
def priceMomentum(productId):
    request_URL = f"https://sky.coflnet.com/api/bazaar/{productId}/snapshot"
    
    timestamp = (datetime.now() - timedelta(hours=6)).isoformat() + "Z"
    response = (requests.get(request_URL, params=timestamp)).json()
    price3SnapshotsAgo = response.get('buyPrice')

    timestamp = (datetime.now()).isoformat() + "Z"
    response = (requests.get(request_URL, params=timestamp)).json()
    currentPrice = response.get('buyPrice')

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
    history = (requests.get(request_URL, params=params)).json()
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
    history = (requests.get(request_URL, params=params)).json()
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
    history = (requests.get(request_URL, params=params)).json()
    netSpreads_List = []
    for entry in history:
        netSpreads_List.append(netSpread(entry['sell'], entry['buy']))
    
    return np.std(netSpreads_List)

#Market Depth Impact
def marketDepthImpact(productId):
    request_URL = f"https://sky.coflnet.com/api/bazaar/{productId}/snapshot"

    timestamp = datetime.now().isoformat() + "Z"
    response = (requests.get(request_URL, params=timestamp)).json()
    orders = response['buyOrders']
    prices = []
    for order in orders:
        prices.append(order['pricePerUnit'])

    maxBuy = prices[0]
    minBuy = prices[-1]
    currentPrice = response['buyPrice']
    
    marketDepthImpact = (maxBuy - minBuy)/(currentPrice)

    return marketDepthImpact

