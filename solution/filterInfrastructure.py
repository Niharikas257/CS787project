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



with open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\infrastructure.json", "r") as f:
    initialInputData = json.load(f)

with open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\infrastructure_team.json", "r") as f:
    inputData = json.load(f)

with open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\shared.json", "r") as f:
    sharedData = json.load(f)

with open("D:/CS787/Project/cs787_ha3_supp_manuf_transp_sn_template 2 (2)/cs787_ha3_supp_manuf_transp_sn_template 2/cs787_ha3_supp_manuf_transp_sn_template/answers/infrastructure_output.json", "r") as f:
    data = json.load(f)  

with open("D:/CS787/Project/cs787_ha3_supp_manuf_transp_sn_template 2 (2)/cs787_ha3_supp_manuf_transp_sn_template 2/cs787_ha3_supp_manuf_transp_sn_template/answers/outOptinfrastructure.json", "r") as f:
    outputData = json.load(f)

def constraints(data):
    return dgal.all([data["full_time"]["qty"] > data["part_time"]["qty"],
                     data["part_time"]["qty"] > data["contract"]["qty"]])

def sortAndRemove(list, category):
    amountToRemove = data["data"][category]["qty"] - outputData["data"][category]["qty"]
    sorted_data = sorted(list, key=lambda x: x["performance_score"], reverse=True)
    sorted_data = sorted_data[:-amountToRemove]
    return sorted_data

list_output = {}

for category in inputData["data"]:
    list_output[category] = []
    list_output_temp = []
    for d in inputData["data"][category]:
        if d["review"] > 8:
            list_output[category].append(d)
        else:
            list_output_temp.append(d)
    list_output_temp = sortAndRemove(list_output_temp, category)
    list_output[category].extend(list_output_temp)

output = {
    "type": inputData["type"],
    "data": list_output
}

with open("answers/outFilterInfrastructure.json", "w") as f:
    json.dump(output, f)

print("Filtering and sorting of Infrastructure department personnel completed.")
