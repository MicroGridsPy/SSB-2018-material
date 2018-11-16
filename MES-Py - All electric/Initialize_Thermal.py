# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 18:18:38 2018

@author: pisto
"""

import pandas as pd

def Initialize_years(model, i):

    '''
    This function returns the value of each year of the project. 
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The year i.
    '''    
    return i

Energy_Demand = pd.read_excel('Example/Demand.xlsx') # open the energy demand file


def Initialize_Demand(model, i, t):
    '''
    This function returns the value of the energy demand from a system for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
        
    :return: The energy demand for the period t.     
        
    '''
    return float(Energy_Demand[i][t])

Thermal_Energy_Demand = pd.read_excel('Example/Thermal_Demand.xlsx') # open the energy thermal demand file

def Initialize_Thermal_Demand(model, i, c, t):
    '''
    This function returns the value of the thermal energy demand from a system for each period and classes of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
        
    :return: The energy demand for the period t.     
        
    '''
    column=i*c;
    
    return float(Thermal_Energy_Demand[column][t])


PV_Energy = pd.read_excel('Example/PV_Energy.xlsx') # open the PV energy yield file

def Initialize_PV_Energy(model, i, t):
    '''
    This function returns the value of the energy yield by one PV under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one PV for the period t.
    '''
    return float(PV_Energy[i][t])

SC_Energy = pd.read_excel('Example/SC_Energy.xlsx') # # open the SC energy yield file

def Initialize_SC_Energy(model, i, c, t):
    '''
    This function returns the value of the energy yield by one SC under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one SC for the class c in the period t.
    '''
    column=i*c;
    
    return float(SC_Energy[column] [t])

def Marginal_Cost_Generator_1(model):
    
    return model.Diesel_Cost/(model.Low_Heating_Value*model.Generator_Effiency)

def Start_Cost(model):
    
    return model.Marginal_Cost_Generator_1*model.Generator_Nominal_Capacity*model.Cost_Increase

def Marginal_Cost_Generator(model):
    
    return (model.Marginal_Cost_Generator_1*model.Generator_Nominal_Capacity-model.Start_Cost_Generator)/model.Generator_Nominal_Capacity 

