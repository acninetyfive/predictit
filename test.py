import numpy as np
import pulp
import urllib.request, json 


data = json.load(open("all.json"))
#print(data)

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

	max_profit = pulp.LpAffineExpression([(lp_vars[x], market.contracts[x].profit) for x in lp_vars])
	max_profit += -850
	c = pulp.LpConstraint(max_profit, -1) 
	problem += c

	return problem


def find_negative_risk(markets):
	negative_risk_markets = {}
	for m in markets:
		p = create_problem(markets[m])
		p.solve()
		if p.objective.value() > 0:
			negative_risk_markets[markets[m].name] = p
	return negative_risk_markets





x_contract = Contract("x", .98)
y_contract = Contract("y", .01)
