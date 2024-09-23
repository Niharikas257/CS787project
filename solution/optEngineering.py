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


# dgal.startDebug()

f = open("D:/CS787/Project/cs787_ha3_supp_manuf_transp_sn_template 2 (2)/cs787_ha3_supp_manuf_transp_sn_template 2/cs787_ha3_supp_manuf_transp_sn_template/answers/developer_output.json", "r")
data = json.loads(f.read())


input = open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\developer.json", "r")
inputData = json.loads(input.read())

shared = open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\shared.json", "r")
sharedData = json.loads(shared.read())

o = open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\optimize_by_percent.json", "r")
optInput = json.loads(o.read())

##check ft qty > pt qty
def constraints(data):
    return dgal.all([
        # data["full_time"]["qty"] > data["part_time"]["qty"] > 0,
        #                 data["part_time"]["qty"] > data["part_time"]["qty"] > 0,
                        data["full_time"]["qty"] >= data["part_time"]["qty"],
                        data["part_time"]["qty"] >= data["contract"]["qty"]])

def findQuantity(category, cost):
    qty = cost / (sharedData["entities"]["engineer"][category]["cost_per_hour"] * inputData["data"]["current"][category]["hour_per_day"])
    return int(qty)


percent = optInput["engineer"]

categories = ["full_time", "part_time", "contract"]
category_costs = {}
total_cost = 0

for category in categories:
    newCost = data["data"][category]["cost"] - data["data"][category]["cost"] * (percent / 100)
    category_costs[category] = {
        "cost": newCost,
        "qty": findQuantity(category, newCost)
    }
    total_cost += newCost


output =  {
    "type": data["type"],
    "cost":total_cost,
    "constraint": constraints(category_costs),
    "data":  category_costs

}

f = open("answers/outOptDeveloper.json","w")
f.write(json.dumps(output))
