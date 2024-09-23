import copy
import collections
import json
import importlib.util
import sys
import shutil
import os
from collections import defaultdict
source_folder = 'D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\lib'
module_name = 'dgalPy'
module_path = source_folder + '/' + module_name + '.py'
spec = importlib.util.spec_from_file_location(module_name, module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
dgal = module

# import aaa_dgalPy.lib.dgalPy as dgal

#--------------------------------------------------------------
# the following is a useful Boolean function returning True if all qty's in newFlow are non-negative
# and greater than or equal to the lower bounds (lb) in flow (inFlow or outFlow)
# replace below with correct implementation if you'd like to use it in analytic models below
def flowBoundConstraint(flow,newFlow):
    # return True
    c1 = dgal.all([newFlow[k]["qty"] >= 0  for k in flow])
    c2 = dgal.all([newFlow[k]["qty"] >= flow[k]["lb"] for k in flow])

    return dgal.all([c1,c2])




def checkNegativeConstraint(flow, newFlow):
    # c = [newFlow[f]["qty"] >= 0 for f in flow]
    # print(flow)
    c1 = dgal.all([newFlow[k]["qty"] >= 0  for k in flow])
    c2 = dgal.all([newFlow[k]["qty"] >= flow[k]["lb"] for k in flow])

    return dgal.all([c1,c2])

    # val = True
    # for k in flow:
    #     if newFlow[k]["qty"] < 0 or  newFlow[k]["qty"] < flow[k]["lb"]:
    #         val = False

    # for k in newFlow:
    #     if newFlow[k]["qty"] < 0 or newFlow[k]["qty"] < flow[k]["lb"]:
    #         val = False

    # return val


def checkHoursConstraint(requirement, current):
    c1 = dgal.all([requirement[k]["lb_hours"] >= 0  for k in requirement])
    c2 = dgal.all([requirement[k]["lb_hours"] <= current[k]["hour_per_day"] for k in requirement])

    return dgal.all([c1,c2])


#--------------------------------------------------------------


def calculateEngineeringCost(developers_data, shared_data):

    # Calculate costs for developers and shared entities
    developers_cost, developers_category_costs = calculate_cost(developers_data, shared_data)

    # Generate JSON output for developers
    developers_output = {
        "type": developers_data["type"],
        "cost": round(developers_cost, 2),
        "constraint": checkHoursConstraint(developers_data["data"]["requirement"], developers_data["data"]["current"]),
        "data": developers_category_costs
    }
    return developers_output


def calculate_cost(data, shared_data):
    categories = ["full_time", "part_time", "contract"]
    total_cost = 0
    category_costs = {}
    type = data["type"]

    for category in categories:
        cost = 0
        hourly_rate = shared_data["entities"][type][category]["cost_per_hour"]
        hours_per_day = data["data"]["current"][category]["hour_per_day"]
        quantity = data["data"]["current"][category]["qty"]

        total_cost += hourly_rate * hours_per_day * quantity
        cost += hourly_rate * hours_per_day * quantity
        category_costs[category] = {
            "qty": round(quantity, 2),
            "cost": round(cost, 2)
        }
    return total_cost, category_costs

#-----------------------------------------------------
# Finance
def finance_metrics(finance_input, shared_input):
    department_type = finance_input["type"]
    data = {}
    total_cost = 0

    for category, details in finance_input['data']['current'].items():
        adjusted_category = category.replace('-', '_')  # Ensure consistent key names
        hourly_rate = shared_input['entities'][department_type][adjusted_category]['cost_per_hour']
        qty = details['qty']
        hours_per_day = details['hour_per_day']
        daily_cost = qty * hours_per_day * hourly_rate
        data[category] = {
            "qty": details['qty'],
            "cost": daily_cost
        }
        total_cost += daily_cost

    def ConstraintEvaluation():
        requirements = finance_input['data']['requirement']
        current = finance_input['data']['current']
        constraints = []

        for category, details in current.items():
            positivity_check = details['qty'] >= 0
            lb_hours = requirements[category].get('lb_hours', 0)
            hour_check = details['hour_per_day'] >= lb_hours
            constraints.append(positivity_check)
            constraints.append(hour_check)
        # constraints = dgal.all([positivity_check,hour_check])
        constraints = dgal.all(constraints)
        return constraints

    constraint = ConstraintEvaluation()
    result = {
        "type": department_type,
        "cost": total_cost,
        "constraint": constraint,
        "data": data
    }
    return result

# Finance end here.
#------------------------------------------------------------
#------------------------------------------------------------
# legal

def legalMetrics(legalInput, shared):
    department_type = legalInput["type"]
    data = {}
    total_cost = 0

    for category, details in legalInput['data']['current'].items():
        adjusted_category = category.replace('-', '_')
        hourly_rate = shared['entities'][department_type][adjusted_category]['cost_per_hour']
        qty=details['qty']
        hours_per_day=details['hour_per_day']
        daily_cost = qty * hours_per_day * hourly_rate
        data[category] = {
            "qty": details['qty'],
            "cost": daily_cost
        }
        total_cost += daily_cost
        
    # constraint = ConstraintEvaluation()
    
    def ConstraintEvaluation():
        requirements = legalInput['data']['requirement']
        current = legalInput['data']['current']
        constraints = []

        for category, details in current.items():
            positivity_check = details['qty'] >= 0
            lb_hours = requirements[category].get('lb_hours', 0)
            hour_check = details['hour_per_day'] >= lb_hours
            constraints.append(positivity_check)
            constraints.append(hour_check)
        # constraints = dgal.all([positivity_check,hour_check])
        constraints = dgal.all(constraints)
        return constraints

    constraint = ConstraintEvaluation()



    result = {
        "type": department_type,
        "cost": total_cost,
        "constraint": constraint,
        "data": data
    }
    return result

#INFRASTRUCTURE DEPARTMENTS HERE

def infrastructureMetrics(infrastructureInput, shared):
    department_type = infrastructureInput["type"]
    data = {}
    total_cost = 0

    for category, details in infrastructureInput['data']['current'].items():
        # adjusted_category = category.replace('-', '_')
        hourly_rate = shared['entities'][department_type][category]['cost_per_hour']
        qty=details['qty']
        hours_per_day=details['hour_per_day']
        daily_cost = qty * hours_per_day * hourly_rate
        data[category] = {
            "qty": details['qty'],
            "cost": daily_cost
        }
        total_cost += daily_cost
        
    def ConstraintEvaluation():
        requirements = infrastructureInput['data']['requirement']
        current = infrastructureInput['data']['current']
        constraints = []

        for category, details in current.items():
            positivity_check = details['qty'] >= 0
            lb_hours = requirements[category].get('lb_hours', 0)
            hour_check = details['hour_per_day'] >= lb_hours
            constraints.append(positivity_check)
            constraints.append(hour_check)
        # constraints = dgal.all([positivity_check,hour_check])
        constraints = dgal.all(constraints)
        return constraints

    constraint = ConstraintEvaluation()
    result = {
        "type": department_type,
        "cost": total_cost,
        "constraint": constraint,
        "data": data
    }
    return result


#MARKETING DEPARTMENT STARTS HERE


def marketingMetrics(marketingInput, shared):
    department_type = marketingInput["type"]
    data = {}
    total_cost = 0
    for category, details in marketingInput['data']['current'].items():
        hourly_rate = shared['entities'][department_type][category]['cost_per_hour']
        qty = details['qty']
        hours_per_day = details['hour_per_day']
        daily_cost = qty * hours_per_day * hourly_rate
        data[category] = {
            "qty": details['qty'],
            "cost": daily_cost
        }
        total_cost += daily_cost

    def ConstraintEvaluation():
        requirements = marketingInput['data']['requirement']
        current = marketingInput['data']['current']
        constraints = []
        for category, details in current.items():
            positivity_check = details['qty'] >= 0
            lb_hours = requirements[category].get('lb_hours', 0)
            hour_check = details['hour_per_day'] >= lb_hours
            constraints.append(positivity_check)
            constraints.append(hour_check)
        return all(constraints)

    constraint = ConstraintEvaluation()

    result = {
        "type": department_type,
        "cost": total_cost,
        "constraint": constraint,
        "data": data
    }
    return result