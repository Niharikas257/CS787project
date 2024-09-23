#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
# sys.path.append(r'//Users/alexbrodsky/Documents/OneDrive\ -\ George\ Mason\ University\ -\ O365\ Production/aaa_python_code')
sys.path.append(r'/lib')
import copy
import pyomo.environ as pyo
from pyomo.environ import *
import json
import ams
# import aaa_dgalPy.lib.dgalPy as dgal
# import importlib.util
# spec = importlib.util.spec_from_file_location("dgal", "/Users/alexbrodsky/Documents/OneDrive - George Mason University - O365 Production/aaa_python_code/aaa_dgalPy/lib/dgalPy.py")
# dgal = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(dgal)

# f = open("example_input_output/shared.json", "r")
f = open("D:\CS787\Project\cs787_ha3_supp_manuf_transp_sn_template 2 (2)\cs787_ha3_supp_manuf_transp_sn_template 2\cs787_ha3_supp_manuf_transp_sn_template\project\shared.json", "r")



shared = json.loads(f.read())

input = json.loads(sys.stdin.read())

#answer = ams.calculateEngineeringCost(input, shared)
#answer = ams.finance_metrics(input, shared)
answer = ams.legalMetrics(input, shared)
#answer = ams.infrastructureMetrics(input, shared)
#answer = ams.marketingMetrics(input, shared)
sys.stdout.write(json.dumps(answer))

# f = open("out.json","w")
# f.write(json.dumps(answer)
#print("\n dgal opt output \n", optAnswer)
#print(json.dumps(optAnswer))
