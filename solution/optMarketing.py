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

# Load JSON Data
with open("D:/CS787/Project/cs787_ha3_supp_manuf_transp_sn_template 2 (2)/cs787_ha3_supp_manuf_transp_sn_template 2/cs787_ha3_supp_manuf_transp_sn_template/answers/marketing_output.json", "r") as f:
    data = json.load(f)

with open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project/marketing.json", "r") as f:
    inputData = json.load(f)

with open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\shared.json", "r") as f:
    sharedData = json.load(f)

with open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\optimize_by_percent.json", "r") as f:
    optPercentInput = json.load(f)

with open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\optimize_by_cost.json", "r") as f:
    optCostInput = json.load(f)

def findQuantity(category, cost):
    cost_per_hour = sharedData["entities"]["marketing"][category]["cost_per_hour"]
    hours_per_day = inputData["data"]["current"][category]["hour_per_day"]
    qty = int(cost / (cost_per_hour * hours_per_day))
    return qty

def constraints(data):
    return dgal.all([
        data["full_time"]["qty"] >= data["part_time"]["qty"],
        data["part_time"]["qty"] >= data["contract"]["qty"]
    ])



def optimizeByPercent():
    percent = optPercentInput["marketing"]
    categories = ["full_time", "part_time", "contract"]
    category_costs = {}
    total_cost = 0

    min_cost_percent = 0.1  

    for category in categories:
        current_cost = data["data"][category]["cost"]
        reduced_cost = current_cost * (1 - (percent / 100))
        
        new_cost = max(reduced_cost, current_cost * min_cost_percent)
        new_qty = findQuantity(category, new_cost)
        new_qty = max(new_qty, 1)  

        category_costs[category] = {
            "cost": round(new_cost),  
            "qty": new_qty
        }
        total_cost += new_cost

    return {
        "type": "marketing",
        "total_cost": round(total_cost), 
        "constraint": constraints(category_costs),
        "data": category_costs
    }


def optimizeByCost():
    cost_limit = optCostInput["marketing"]
    categories = ["full_time", "part_time", "contract"]
    category_costs = {}
    total_cost = 0
    initial_total_cost = sum(data["data"][cat]["cost"] for cat in categories)
    remaining_cost = cost_limit

    for category in categories:
        if initial_total_cost > 0:
            proportion = data["data"][category]["cost"] / initial_total_cost
            target_cost = max(proportion * cost_limit, 0)
        else:
            target_cost = 0

        
        adjusted_cost = min(target_cost, remaining_cost)
        adjusted_cost = round(adjusted_cost)  

        new_qty = findQuantity(category, adjusted_cost)
        new_qty = int(new_qty)  
        category_costs[category] = {
            "cost": adjusted_cost,
            "qty": new_qty
        }
        total_cost += adjusted_cost
        remaining_cost -= adjusted_cost  

    return {
        "type": "marketing",
        "total_cost": round(total_cost),  
        "constraint": constraints(category_costs),
        "data": category_costs
    }




# Choose optimization method here
output = optimizeByPercent()  
#output = optimizeByCost()

with open("answers/outOptMarketing.json", "w") as f:
    json.dump(output, f)
