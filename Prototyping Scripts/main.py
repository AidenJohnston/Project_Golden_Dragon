import bazaarFunctions as bf
import pandas as pd
import numpy as np
import requests

###inputs
#budget = input("Enter your budget: $ ")
#risk_tolerance = input("Enter your risk tolerance (low, medium, high): ")
#holding_horizon = input("Enter your holding horizon (quick-flip (0) or hold (1)): ")


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
#daily commit on 2/10/2026





