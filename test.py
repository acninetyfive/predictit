import numpy as np
import pulp
import urllib.request, json 

'''
with urllib.request.urlopen("https://www.predictit.org/api/marketdata/all/") as url:
    data = json.loads(url.read().decode())
    print(data)
'''

class Bet:
	def __init__(self, name, cost):
		self.name = name
		self.cost = cost
		self.profit = round(.9 * (1 - cost), 3)


def create_problem(bets):
	lp_vars = {}

	problem = pulp.LpProblem("Problem", pulp.LpMaximize)

	profit = pulp.LpVariable('profit', lowBound=0, cat='Continuous')
	
	problem += profit
	
	for b in bets:
		lp_vars[bets[b].name] = pulp.LpVariable(bets[b].name, lowBound=0, cat='Integer')
	
	#print(lp_vars)
	for v in lp_vars:
		if v is not "profit":
			expr = pulp.LpAffineExpression([(lp_vars[x], bets[x].profit) if x != v else (lp_vars[x], -1 * bets[x].cost) for x in lp_vars] + [(profit, -1)])
			c = pulp.LpConstraint(expr, 1) #1 indicates the expression should be >= 0
			problem += c

	max_profit = pulp.LpAffineExpression([(lp_vars[x], bets[x].profit) for x in lp_vars])
	max_profit += -850
	c = pulp.LpConstraint(max_profit, -1) 
	problem += c

	return problem

x_bet = Bet("x", .98)
y_bet = Bet("y", .01)


nom_bets = {"kamala": Bet("kamala", .75), "biden": Bet("biden", .80), "warren": Bet("warren", .82), 
		"sanders": Bet("sanders", .87), "buttigieg": Bet("buttigieg", .88), "yang": Bet("yang", .93),
		"booker": Bet("booker", .98), "gabbard": Bet("gabbard", .98), "castro": Bet("castro", .97),
		"klobuchar": Bet("klobuchar", .98), "orourke": Bet("orourke", .98), "clinton": Bet("clinton", .98),
		"a": Bet("a", .99), "b": Bet("b", .99), "c": Bet("c", .99), "d": Bet("d", .99), "e": Bet("e", .99)}

pres_bets = {"trump": Bet("trump", .56), "kamala": Bet("kamala", .84), "biden": Bet("biden", .87), "warren": Bet("warren", .88), 
		"sanders": Bet("sanders", .92), "buttigieg": Bet("buttigieg", .92), "yang": Bet("yang", .94),
		"booker": Bet("booker", .96), "gabbard": Bet("gabbard", .96), "a": Bet("a", .99), "b": Bet("b", .99), "c": Bet("c", .99)}


problem = create_problem(pres_bets)

#print(problem)

print(problem.solve())

for variable in problem.variables():
	print(variable.name, variable.varValue)




#API Call for all markets
#https://www.predictit.org/api/marketdata/all/
