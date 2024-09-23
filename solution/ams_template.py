import copy
import json
import importlib.util
import sys

# sys.path.append("/Users/alexbrodsky/Documents/OneDrive - George Mason University - O365 Production/aaa_python_code/aaa_dgalPy")
# replace path below to the path to the provided folder
sys.path.append("/Users/alexbrodsky/Documents/OneDrive - George Mason University - O365 Production/aaa_python_code/cs787_ha3_supp_manuf_transp_sn_solution")

import lib.dgalPy as dgal

# import aaa_dgalPy.lib.dgalPy as dgal

#--------------------------------------------------------------
# the following is a useful Boolean function returning True if all qty's in newFlow are non-negative
# and greater than or equal to the lower bounds (lb) in flow (inFlow or outFlow)
# replace below with correct implementation if you'd like to use it in analytic models below
def flowBoundConstraint(flow,newFlow):
    return True

#--------------------------------------------------------------

def am(input):
    shared = input["shared"]
    root = input["rootService"]
    services = input["services"]

    serviceMetrics = computeMetrics(shared,root,services)

    cost = serviceMetrics[root]["cost"]
    constraints = serviceMetrics[root]["constraints"]

    return {
        "cost": cost, "constraints": constraints,
        "rootService": root, "services": serviceMetrics
    }
#--------------------------------------------------------------------
#assumptions on input data for ns:computeMetrics:
#1. root service inFlows and outFlows are disjoint
#2. every inFlow of every subService must have a corresponding root inFlow
#   and/or a corresponding subService outFlow (i.e., an inFlow of a subService can't
#   come from nowhere)
#3. every outFlow of every subService must have a corresponding root outFlow
#   and/or a corresponding subService inFlows (i.e., an outFlow of a subService can't
#  go nowhere)
#4. every root outFlow must have at least one corresponding subService outFlow
#5. every root inFlow must have at least one corresponding subService inFlow
#----------------------------------------------------------------

def computeMetrics(shared,root,services):
    type = services[root]["type"]
    inFlow = services[root]["inFlow"]
    outFlow = services[root]["outFlow"]

    if type == "supplier":
        return {root: supplierMetrics(services[root])}
    elif type == "manufacturer":
        return {root: manufMetrics(services[root])}
    elif type == "transport":
        return {root: transportMetrics(services[root],shared)}
    else:
        subServices = services[root]["subServices"]
        subServiceMetrics = dgal.merge([computeMetrics(shared,s,services) for s in subServices])
#--------------------
# replace below with a correct cost computation
        cost = 1000
#--------------------
# compute the set union of inFlow and outFlow keys of the root service
        inOutFlowKeysSet = {"tbd"}
#--------------------
# compute the set of all flow ids from
# inFlow and outFlow of the root service, as well as from inFlow and outFlow of all subServices
        flowKeysSet = {"tbd"}
#--------------------
# below is the set of flow ids from inFlow and outFlow of subServices, so that these
# flow ids do not appear in inFlow or outFlow of the root service
        internalOnlyFlowKeysSet = set(flowKeysSet).difference(inOutFlowKeysSet)
#--------------------
# below complete/fix the computation of the dictionary subServiceFlowSupply,
# which gives, for every flow f in flowKeysSet, the total quantity of flow f
# coming from all subServices in their outFlow

        subServicesFlowSupply = dict()
        for f in flowKeysSet:
            supply = 1000
            subServicesFlowSupply.update({f: supply})
#--------------------
# below complete/fix the computation of the dictionary subServiceFlowDemand,
# which gives, for every flow f in flowKeysSet, the total quantity of flow f
# coming into all subServices in their inFlow

        subServicesFlowDemand = dict()
        for f in flowKeysSet:
            demand = 1000
            subServicesFlowDemand.update({f: demand})
#--------------------
# below complete/fix the computation of newInFlow,
# which is a dictionary with the same keys as inFlow;
# for every key f in inFlow, the value in newInFlow is a dictionary of the form
# {"qty": qty, "item": item}, where item is taken from inFlow,
# and you need to correctly compute qty
# (hint: use subServicesFlowSupply and subServicesFlowDemand)

        newInFlow = dict()
        for f in inFlow:
            qty = 1000
            newInFlow.update({f:{"qty":qty, "item": inFlow[f]["item"]}})
#--------------------
# below complete/fix the computation of newOutFlow,
# which is a dictionary with the same keys as outFlow;
# for every key f in outFlow, the value in newOutFlow is a dictionary of the form
# {"qty": qty, "item": item}, where item is taken from outFlow,
# and you need to correctly compute qty
# (hint: use subServicesFlowSupply and subServicesFlowDemand)
        newOutFlow = dict()
        for f in outFlow:
            qty = 1000
            newOutFlow.update({f:{"qty":qty, "item": outFlow[f]["item"]}})
#        dgal.debug("newInFlow",newInFlow)
#---------------------
# below complete/fix the computation of constraint (must return Boolean value)
# that for every flow f in internalOnlyFlowKeysSet, the total "supplied" qty of f,
# i.e., coming from all subServices in their outFlow, is greater then or equal
# the total "demand" qty of f, i.e., coming into all subServices in their inFlow
        internalSupplySatisfiesDemand = dgal.all([
            True
            for f in internalOnlyFlowKeysSet
        ])
#---------------------
# below are the flowBoundConstraints, which use the corresponding function
# you need to implement - see above

        inFlowConstraints = flowBoundConstraint(inFlow,newInFlow)
        outFlowConstraints = flowBoundConstraint(outFlow,newOutFlow)
        subServiceConstraints = dgal.all([ subServiceMetrics[s]["constraints"]
                                        for s in subServices
                                ])
        constraints = dgal.all([ internalSupplySatisfiesDemand,
                            inFlowConstraints,
                            outFlowConstraints,
                            subServiceConstraints
                      ])
        dgal.debug("constraints", constraints)
        rootMetrics = {
            root : {
                "type": type,
                "cost": cost,
                "constraints": constraints,
                "inFlow": newInFlow,
                "outFlow": newOutFlow,
                "subServices": subServices
            }
        }
        return dgal.merge([ subServiceMetrics , rootMetrics ])

# end of Compute Metrics function
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
def supplierMetrics(supInput):
    type = supInput["type"]
    inFlow = supInput["inFlow"]
    outFlow = supInput["outFlow"]

# replace below with correct computation

    cost = 1000

    newOutFlow = "TBD"

    constraints = flowBoundConstraint(outFlow,newOutFlow)
    return {
        "type": type,
        "cost": cost,
        "constraints": constraints,
        "inFlow": dict(),
        "outFlow": newOutFlow
    }
#---------------------------------------------------------------------------------------
# simple manufacturer
# assumption: there is an input flow for every inQtyPer1out

def manufMetrics(manufInput):
    type = manufInput["type"]
    inFlow = manufInput["inFlow"]
    outFlow = manufInput["outFlow"]
    qtyInPer1out = manufInput["qtyInPer1out"]
# replace below with correct computation
    cost = 1000
    newInFlow = "TBD"
    newOutFlow = "TBD"

    inFlowConstraints = flowBoundConstraint(inFlow,newInFlow)
    outFlowConstraints = flowBoundConstraint(outFlow,newOutFlow)
    constraints = dgal.all([ inFlowConstraints, outFlowConstraints])

    return { "type": type,
             "cost": cost,
             "constraints": constraints,
             "inFlow": newInFlow,
             "outFlow": newOutFlow
    }
# end of manufMetrics
#--------------------------------------------------
def transportMetrics(transportInput, shared):
    type = transportInput["type"]
    inFlow = transportInput["inFlow"]
    outFlow = transportInput["outFlow"]
    pplbFromTo = transportInput["pplbFromTo"]
    orders = transportInput["orders"]
# replace below with correct implementation. Note: it is based on transportation orders
    newInFlow = "TBD"
    newOutFlow = "TBD"
# replace below with computation of all source locations
    sourceLocations = "TBD"
# replace below with computation of a structure for all source-destination pairs in orders
    destsPerSource = "TBD"
# replace below with computation of total weight for every source-destination pair according to orders
    weightCostPerSourceDest = "TBD"
# replace below with transportation cost computation, based on, for each source-destination pair,
# on total weight and price per pound (pplb)
    cost = 1000

    inFlowConstraints = flowBoundConstraint(inFlow,newInFlow)
    outFlowConstraints = flowBoundConstraint(outFlow,newOutFlow)
    constraints = dgal.all([inFlowConstraints,outFlowConstraints])
    return { "type": type,
             "cost": cost,
             "constraints": constraints,
             "inFlow": newInFlow,
             "outFlow": newOutFlow
    }

#-------------------------------
# do not touch the part below; the function am above
# is more general than the functions below

def combinedSupply(input):
    return am(input)
def combinedManuf(input):
    return am(input)
def combinedTransp(input):
    return am(input)
