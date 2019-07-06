import numpy as np
import pulp
import json 
import requests
from requests.exceptions import HTTPError


class Market:
	def __init__(self, data):
		self.id = data["id"]
		self.name = data["shortName"]
		self.contracts = {c["shortName"]: Contract(c["shortName"], c["bestBuyNoCost"]) for c in data["contracts"] if c["bestBuyNoCost"] is not None}

class Contract:
	def __init__(self, name, cost):
		self.name = name
		self.cost = cost
		self.profit = round(.9 * (1 - cost), 3)


def load_markets(data):
	markets = {}
	for item in data["markets"]:
		markets[item["shortName"]] = Market(item)
	return markets


def create_problem(market):
	lp_vars = {}

	problem = pulp.LpProblem(market.name, pulp.LpMaximize)

	profit = pulp.LpVariable('profit', lowBound=0, cat='Continuous')
	
	problem += profit
	
	for c in market.contracts:
		lp_vars[market.contracts[c].name] = pulp.LpVariable(market.contracts[c].name, lowBound=0, cat='Integer')
	
	#print(lp_vars)
	for v in lp_vars:
		if v is not "profit":
			expr = pulp.LpAffineExpression([(lp_vars[x], market.contracts[x].profit) if x != v else (lp_vars[x], -1 * market.contracts[x].cost) for x in lp_vars] + [(profit, -1)])
			c = pulp.LpConstraint(expr, 1) #1 indicates the expression should be >= 0
			problem += c
			problem += lp_vars[v] * market.contracts[v].cost <= 850 

	#max_profit = pulp.LpAffineExpression([(lp_vars[x], market.contracts[x].profit) for x in lp_vars])
	#max_profit += -850
	#c = pulp.LpConstraint(max_profit, -1) 
	#problem += c

	return problem


def find_negative_risk(markets):
	negative_risk_markets = {}
	for m in markets:
		p = create_problem(markets[m])
		p.solve()
		if p.objective.value() > 0:
			negative_risk_markets[markets[m].name] = p
	return negative_risk_markets


url = "https://www.predictit.org/api/marketdata/all/"
try:
	response = requests.get(url)

	# If the response was successful, no Exception will be raised
	response.raise_for_status()
except HTTPError as http_err:
	print(f'HTTP error occurred: {http_err}')  # Python 3.6
except Exception as err:
	print(f'Other error occurred: {err}')  # Python 3.6
else:
	print('Success!')

data = json.loads(response.content)

markets = load_markets(data)

nr = find_negative_risk(markets)

for item in nr:
	if nr[item].objective.value() > 0:
		print(item, nr[item].objective.value())
		for v in nr[item].variables():
			print(v, v.value())
	print()
