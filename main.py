import bazaarFunctions as bf
import pandas as pd
import numpy as np
import requests

#inputs
budget = input("Enter your budget: $ ")
risk_tolerance = input("Enter your risk tolerance (low, medium, high): ")
holding_horizon = input("Enter your holding horizon (quick-flip (0) or hold (1)): ")


#turning the risk tolerance into alpha
if risk_tolerance == "low":
    alpha = 1.5
elif risk_tolerance == "medium":
    alpha = 1.0
elif risk_tolerance == "high":
    alpha = 0.5

#get the entirety of the bazaar
bazaar_url = "https://api.hypixel.net/v2/skyblock/bazaar"
items = bf.get_bazaar_list(bf.get_bazaar_data(bazaar_url))

# clear out the useless items
#i'll do this one later

###number crunching
#bid/ask spread
bidAsk_spread = []
for item in items:
    spread = bf.bidAskSpread(item)
    print(spread)
    bidAsk_spread.append(spread)


#liquidity

#volatility

#stability score

#affordability

#event sensitivity (optional for now)



###scoring function
#Expected profit = Spread * FillProbability * ScaleFactor

#RiskPenalty = (alpha * Volatility) + (beta * EventRisk) + (gamma * LowLiquidPenalty)

#Score = (ExpectedProfit - RiskPenalty) * RiskToleranceMultiplier


#Sort the entire list by score (lowkey the algorithmic runtime of this has got to be shit but idc anymore)


###output (top 5 opportunities)
#Item Tag, Expected Return, Volatility, Fill Probability, and Suggested Action



