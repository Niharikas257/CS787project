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

f = open("D:/CS787/Project/cs787_ha3_supp_manuf_transp_sn_template 2 (2)/cs787_ha3_supp_manuf_transp_sn_template 2/cs787_ha3_supp_manuf_transp_sn_template/answers/finance_output.json", "r")
data = json.loads(f.read())


input = open("D:/CS787/Project/cs787_ha3_supp_manuf_transp_sn_template 2 (2)/cs787_ha3_supp_manuf_transp_sn_template 2/cs787_ha3_supp_manuf_transp_sn_template/project/finance_team.json", "r")
inputData = json.loads(input.read())

initialInput = open("D:/CS787/Project/cs787_ha3_supp_manuf_transp_sn_template 2 (2)/cs787_ha3_supp_manuf_transp_sn_template 2/cs787_ha3_supp_manuf_transp_sn_template/project/finance.json", "r")
initialInputData = json.loads(initialInput.read())

output = open("D:/CS787/Project/cs787_ha3_supp_manuf_transp_sn_template 2 (2)/cs787_ha3_supp_manuf_transp_sn_template 2/cs787_ha3_supp_manuf_transp_sn_template/answers/outOptFinance.json", "r")
outputData = json.loads(output.read())

shared = open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\shared.json", "r")
sharedData = json.loads(shared.read())



##check ft qty > pt qty
def constraints(data):
    return dgal.all([data["full_time"]["qty"] > data["part_time"]["qty"], data["part_time"]["qty"] > data["contract"]["qty"]])

def findQuantity(category, cost):
    qty = cost / (sharedData["entities"]["engineer"][category]["cost_per_hour"] * inputData["data"]["current"][category]["hour_per_day"])
    return int(qty)

def sortAndRemove(list, category):
    amountToRemove = initialInputData["data"]["current"][category]["qty"] - outputData["data"][category]["qty"]
    sorted_data = sorted(list, key=lambda x: x["score"])
    sorted_data = sorted_data[:-amountToRemove]
    return sorted_data



list_output = {}
list_output_temp= []

weights = sharedData["entities"]["weights"]

for category in inputData["data"]:
    list_output[category] = []
    list_output_temp= []
    for d in inputData["data"][category]:
        weight = (d["review"] * weights["review"]) +  (d["experience"] * weights["experience"])
        if d["review"] >= 9:
            list_output[category].append({
                "score": round(weight,3),
                "name": d["name"]
            })
        else:
            list_output_temp.append({
                "score": round(weight,3),
                "name": d["name"]
            })
    list_output_temp =  sortAndRemove(list_output_temp, category)
    list_output[category].extend(list_output_temp)

output =  {
    "type": inputData["type"],
    # "constraint": constraints(list_output)
    "data": list_output
}

f = open("answers/outFilterFinance.json","w")
f.write(json.dumps(output))
