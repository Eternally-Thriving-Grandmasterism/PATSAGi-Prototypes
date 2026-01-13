from pulp import *

def allocate_resources(needs, resources):
    prob = LpProblem("Abundance_Optimization", LpMaximize)
    allocations = LpVariable.dicts("Alloc", needs.keys(), lowBound=0)

    # Objective: Maximize collective joy (weighted by need satisfaction)
    prob += lpSum(allocations[i] * needs[i]['joy_weight'] for i in needs)

    # Constraints: Resource limits + minimum need fulfillment
    for res, amount in resources.items():
        prob += lpSum(allocations[i] * needs[i]['costs'].get(res, 0) for i in needs) <= amount

    for i in needs:
        prob += allocations[i] >= needs[i]['minimum']

    prob.solve()
    return {i: value(allocations[i]) for i in needs if value(allocations[i]) > 0}
