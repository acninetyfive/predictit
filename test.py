import numpy as np
from pulp import *

class Bet:
	def __init__(self, name, cost):
		self.name = name
		self.cost = cost
		self.profit = round(.9 * (1 - cost), 3)


def create_problem(bets):
	lp_vars = []

	problem = pulp.LpProblem("Problem", LpMaximize)

	for b in bets:
		lp_vars.append(pulp.LpVariable(b.name, lowBound=0, cat='Integer'))
	lp_vars.append(pulp.LpVariable('profit', lowBound=0, cat='Continuous'))



x_bet = Bet("x", .98)
y_bet = Bet("y", .01)






test_problem = pulp.LpProblem("Test", LpMaximize)


x = pulp.LpVariable('x', lowBound=0, cat='Integer')
y = pulp.LpVariable('y', lowBound=0, cat='Integer')
z = pulp.LpVariable('z', lowBound=0, cat='Continuous')

#objective
test_problem += z, "Z"


# Constraints
test_problem += x_bet.profit * x - y_bet.cost * y >= z
test_problem += -x_bet.cost * x + y_bet.profit * y >= z 
test_problem += x_bet.profit * x + y_bet.profit * y <= 850

test_problem.solve()

for variable in test_problem.variables():
	print(variable.name, variable.varValue)






