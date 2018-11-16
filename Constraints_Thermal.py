# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:41:38 2018

@author: pisto
"""

# Thermal Model 
# Objective funtion

def Net_Present_Cost(model): # OBJETIVE FUNTION: MINIMIZE THE NPC FOR THE SISTEM
    '''
    This function computes the sum of the multiplication of the net present cost 
    NPC (USD) of each scenario and their probability of occurrence.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
      
    return (sum(model.Scenario_Net_Present_Cost[i]*model.Scenario_Weight[i] for i in model.scenario ))
      
############################################## PV constraints ##################################################

def Solar_Energy(model,i,t): # Energy output of the solar panels
    '''
    This constraint calculates the energy produce by the solar panels taking in 
    account the efficiency of the inverter for each scenario.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_Energy_PV[i,t] == model.PV_Energy_Production[i,t]*model.Inverter_Efficiency*model.PV_Units

###################################################### SC constraints ######################################

def Solar_Thermal_Energy (model,i,c,t): # Energy output of solar collectors

    '''
    This constraint calculates the energy produced by the solar collectors 
    for each scenario considering all the users for each class (indicated by the parameter "c")
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_Energy_SC [i,c,t] == model.SC_Energy_Production[i,c,t]*model.SC_Units[c]


############################################## Battery constraints #############################################

def State_of_Charge(model,i, t): # State of Charge of the battery
    '''
    This constraint calculates the State of charge of the battery (State_Of_Charge) 
    for each period of analysis. The State_Of_Charge is in the period 't' is equal to
    the State_Of_Charge in period 't-1' plus the energy flow into the battery, 
    minus the energy flow out of the battery. This is done for each scenario i.
    In time t=1 the State_Of_Charge_Battery is equal to a fully charged battery.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    if t==1: # The state of charge (State_Of_Charge) for the period 0 is equal to the Battery size.
        return model.State_Of_Charge_Battery[i,t] == model.Battery_Nominal_Capacity*1 - model.Energy_Battery_Flow_Out[i,t]/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[i,t]*model.Charge_Battery_Efficiency
    if t>1:  
        return model.State_Of_Charge_Battery[i,t] == model.State_Of_Charge_Battery[i,t-1] - model.Energy_Battery_Flow_Out[i,t]/model.Discharge_Battery_Efficiency + model.Energy_Battery_Flow_In[i,t]*model.Charge_Battery_Efficiency    

def Maximun_Charge(model, i, t): # Maximun state of charge of the Battery
    '''
    This constraint keeps the state of charge of the battery equal or under the 
    size of the battery for each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.State_Of_Charge_Battery[i,t] <= model.Battery_Nominal_Capacity

def Minimun_Charge(model,i, t): # Minimun state of charge
    '''
    This constraint maintains the level of charge of the battery above the deep 
    of discharge in each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.State_Of_Charge_Battery[i,t] >= model.Battery_Nominal_Capacity*model.Deep_of_Discharge

def Max_Power_Battery_Charge(model): 
    '''
    This constraint calculates the Maximum power of charge of the battery. Taking in account the 
    capacity of the battery and a time frame in which the battery has to be fully loaded for 
    each scenario.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximun_Charge_Power== model.Battery_Nominal_Capacity/(model.Maximun_Battery_Charge_Time/model.Delta_Time)

def Max_Power_Battery_Discharge(model):
    '''
    This constraint calculates the Maximum power of discharge of the battery. for 
    each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximun_Discharge_Power == model.Battery_Nominal_Capacity/(model.Maximun_Battery_Discharge_Time/model.Delta_Time)

def Max_Bat_in(model, i, t): # Minimun flow of energy for the charge fase
    '''
    This constraint maintains the energy in to the battery, below the maximum power 
    of charge of the battery for each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_In[i,t] <= model.Maximun_Charge_Power

def Max_Bat_out(model,i, t): #minimun flow of energy for the discharge fase
    '''
    This constraint maintains the energy from the battery, below the maximum power of 
    discharge of the battery for each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Battery_Flow_Out[i,t] <= model.Maximun_Discharge_Power

####################################################### TANK constraints ####################################

def State_Of_Charge_Tank (model,i,c,t): # State of Charge (SOC) of the thermal storage (Tank)
    '''
     This constraint calculates the state of charge of the thermal storage (tank)
     for each period of analysis and for each class of users. It is an energy
     balance on the hot water storage tank unit in each period. The SOC_Tank 
     in the period 't' is equal to the SOC_Tank in the period 't-1' plus the energy
     flow into the tank, minus the energy flow out of the tank, plus the resistance heat, curtailment and losses. This is done for each
     class c and scenario i. In time t=1 the SOC_Tank is equal to a fully charged tank.
     :param model: Pyomo model as defined in the Model_creation library.
     '''
    if t==1: # SOC_Tank  for the period 0 is equal to the Tank size.
        return model.SOC_Tank[i,c,t] == model.Tank_Nominal_Capacity[c]*1 + model.Total_Energy_SC [i,c,t] + model.Resistance_Thermal_Energy [i,c,t]*model.Electric_Resistance_Efficiency - model.Energy_Tank_Flow_Out[i,c,t] 

    if t>1:  
        return model.SOC_Tank [i,c,t] == model.SOC_Tank[i,c,t-1]*model.Tank_Efficiency + model.Total_Energy_SC [i,c,t] + model.Resistance_Thermal_Energy [i,c,t]*model.Electric_Resistance_Efficiency - model.Energy_Tank_Flow_Out[i,c,t] 


def Maximun_Tank_Charge(model,i,c,t): # Maximun state of charge of the Tank in terms of thermal energy
    '''
    This constraint keeps the state of charge of the tank equal or under the 
    size of the tank for each scenario i and each class c.
    
    :param model: Pyomo model as defined in the Model_creation library.    
    '''
    return model.SOC_Tank[i,c,t] <= model.Tank_Nominal_Capacity[c]

def Minimun_Tank_Charge(model,i,c,t): # Minimun state of charge
    '''
    This constraint maintains the level of charge of the battery above the deep 
    of discharge in each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.SOC_Tank [i,c,t] >= model.Tank_Nominal_Capacity[c]*model.Deep_of_Tank_Discharge

def Max_Power_Tank_Discharge(model,c):
    '''
    This constraint calculates the Maximum power of discharge of the battery. for 
    each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Maximun_Tank_Discharge_Power[c] == model.Tank_Nominal_Capacity[c]/(model.Maximun_Tank_Discharge_Time/model.Delta_Time)

def Max_Tank_out(model,i,c, t): #minimun flow of energy for the discharge fase
    '''
    This constraint maintains the energy from the battery, below the maximum power of 
    discharge of the battery for each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Tank_Flow_Out[i,c,t] <= model.Maximun_Tank_Discharge_Power[c]


################################### Electrical Resistance #####################################################

def Maximum_Resistance_Thermal_Energy (model,i,c,t):
    '''
    This constraint calculates the total thermal energy produced by the electrical resistance
    for each scenario i and class c.
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Resistance_Thermal_Energy [i,c,t] <= model.Nominal_Power_Resistance[c] #*model.Resistance_Units[c]

############################## Boiler constraints ############################

def Maximum_Boiler_Energy(model,i,c,t): # Maximun energy output of the Boiler    
    '''
    This constraint ensures that the boiler will not exceed his nominal capacity 
    in each period in each scenario i and class c.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Boiler_Energy[i,c,t] <= model.Boiler_Nominal_Capacity[c]

def NG_Consumption(model,i,c,t): # NG comsuption 
    '''
    This constraint transforms the energy produced by the boiler generator into 
    kg of natural gas in each scenario i and class c.
    This is done using the lower heating value (LHV)
    of the natural gas and the efficiency of the boiler.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.NG_Consume[i,c,t] == model.Boiler_Energy [i,c,t]/(model.Boiler_Efficiency*(model.Low_Heating_Value_NG/model.Delta_Time))

############################################## Energy Constraints ###############################################

def Total_Thermal_Energy_Demand (model, i, c, t):
    ''' 
    This constraint calculates the thermal energy demand for all the users in each classs c and for each scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Total_Thermal_Energy_Demand[i,c,t] == (model.Thermal_Energy_Demand[i,c,t]*model.Users_Number_Class[c])

def Thermal_Energy_Balance(model,i,c,t): # Thermal energy balance
     '''
     This costraint ensures the perfect match between the energy demand of the 
     system and the different sources to meet the thermal energy demand for each class c 
     and each scenario i
     :param model: Pyomo model as defined in the Model_creation library.
     '''
     return  model.Total_Thermal_Energy_Demand[i,c,t] == model.Boiler_Energy[i,c,t]  + model.Energy_Tank_Flow_Out[i,c,t] - model.Thermal_Energy_Curtailment[i,c,t] + model.Lost_Load_Th[i,c,t]

def Total_Electrical_Resistance_Demand (model,i,t): # The summation of the electrical resistance demand of each class. 
     '''
     This constraint defines the electrical demand that comes from the 
     electrical resistance to satisfy the thermal demand. 
     This term is involved in the electrical energy balance.
     :param model: Pyomo model as defined in the Model_creation library.
     '''
     return model.Total_Electrical_Resistance_Demand[i,t] == sum(model.Resistance_Thermal_Energy[i,c,t] for c in model.classes)

def Energy_balance(model, i, t): # Energy balance
    '''
    This constraint ensures the perfect match between the energy energy demand of the 
    system and the differents sources to meet the energy demand including 
    the electric resistance demand of thermal part each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Energy_Demand[i,t] == model.Total_Energy_PV[i,t] + model.Generator_Energy[i,t] - model.Energy_Battery_Flow_In[i,t] + model.Energy_Battery_Flow_Out[i,t] + model.Lost_Load[i,t] - model.Energy_Curtailment[i,t] - model.Total_Electrical_Resistance_Demand[i,t]

def Maximun_Lost_Load(model,i): # Maximum permissible lost load
    '''
    This constraint ensures that the ratio between the lost load and the energy 
    Demand does not exceeds the value of the permisible lost load each scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Lost_Load_Probability >= (sum(model.Lost_Load[i,t] for t in model.periods)/sum(model.Energy_Demand[i,t] for t in model.periods))

def Maximun_Lost_Load_Th(model,i,c): # Maximum permissible lost load thermal
    '''
    This constraint ensures that the ratio between the lost load and the energy 
    Demand does not exceeds the value of the permisible lost load each scenario i and class c. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Lost_Load_Probability*sum(model.Total_Thermal_Energy_Demand[i,c,t] for t in model.periods) >= sum(model.Lost_Load_Th[i,c,t] for t in model.periods)
######################################## Diesel generator constraints #################################################################

def Maximun_Diesel_Energy(model,i, t): # Maximun energy output of the diesel generator
    '''
    This constraint ensures that the generator will not exceed his nominal capacity 
    in each period in each scenario i.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Generator_Energy[i,t] <= model.Generator_Nominal_Capacity

def Diesel_Comsuption(model,i, t): # Diesel comsuption 
    '''
    This constraint transforms the energy produce by the diesel generator in to 
    liters of diesel in each scenario i.This is done using the low heating value
    of the diesel and the efficiency of the diesel generator.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Diesel_Consume[i,t] == model.Generator_Energy[i,t]/(model.Generator_Efficiency*(model.Low_Heating_Value/model.Delta_Time))
                                                                                                                                  
                                                                 
############################################## Economical Constraints ###################################################
    
def SC_Financial_Cost(model):
   '''
   This constraint defines the financial cost of the solar collector technology 
   as the summation of each class that will be considered in the Financial Cost. 
   In this way all costs of each class will be considered.
   :param model: Pyomo model as defined in the Model_creation library.
   '''
   return model.SC_Financial_Cost == sum(model.SC_Units[c]*model.SC_investment_Cost*model.SC_Nominal_Capacity for c in model.classes)

def Tank_Financial_Cost (model):
   '''
   This constraint defines the financial cost of the tank technology 
   as the summation of each class that will be considered in the Financial Cost.
   In this way all costs of each class will be considered.
   :param model: Pyomo model as defined in the Model_creation library.
   '''
   return model.Tank_Financial_Cost == sum(model.Tank_Nominal_Capacity[c]*model.Tank_Invesment_Cost*model.Delta_Time for c in model.classes)

def Boiler_Financial_Cost (model):
   ''' 
   This constraint defines the financial cost of the boiler technology 
   as the summation of each class that will be considered in the Financial Cost.
   In this way all costs of each class will be considered.
   :param model: Pyomo model as defined in the Model_creation library.
   '''
   return model.Boiler_Financial_Cost == sum(model.Boiler_Nominal_Capacity[c]*model.Boiler_Invesment_Cost for c in model.classes)

def Resistance_Financial_Cost (model):
   ''' 
   This constraint defines the financial cost of the resistance technology 
   as the summation of each class that will be considered in the Financial Cost.
   In this way all costs of each class will be considered.
   :param model: Pyomo model as defined in the Model_creation library.
   '''
   return model.Resistance_Financial_Cost == sum(model.Nominal_Power_Resistance[c]*model.Resistance_Invesment_Cost for c in model.classes)


def Financial_Cost(model): 
    '''
    This constraint calculates the yearly payment for the borrow money.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    return model.Cost_Financial == ((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Delta_Time + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost + model.SC_Financial_Cost + model.Tank_Financial_Cost + model.Boiler_Financial_Cost + model.Resistance_Financial_Cost)*model.Porcentage_Funded*model.Interest_Rate_Loan)/(1-((1+model.Interest_Rate_Loan)**(-model.Years)))

def Diesel_Cost_Total(model,i):
    '''
    This constraint calculates the total cost due to the use of diesel to generate 
    electricity in the generator in each scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    foo=[]
    for f in range(1,model.Periods+1):
        foo.append((i,f))
    return model.Diesel_Cost_Total[i] == sum(((sum(model.Diesel_Consume[i,t]*model.Diesel_Unitary_Cost for i,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
    
def NG_Cost_Total (model,i):
    '''
    This constraint calculates the total cost due to the use of Natural Gas to generate 
    thermal energy in the boiler in each scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    foo=[] 
    for c in range (1,model.Classes+1): 
        for f in range(1,model.Periods+1):
            foo.append((i,c,f))
    return  model.NG_Cost_Total[i] == sum(((sum(model.NG_Consume[i,c,t]*model.NG_Unitary_Cost for i,c,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years)
                                                                     
def Scenario_Lost_Load_Cost(model, i):
    '''
    This constraint calculates the cost due to the lost load in each scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''
    foo=[]
    for f in range(1,model.Periods+1):
        foo.append((i,f))
        
    return  model.Scenario_Lost_Load_Cost[i] == sum(((sum(model.Lost_Load[i,t]*model.Value_Of_Lost_Load*model.Delta_Time for i,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
 

def Scenario_Lost_Load_Cost_Th (model,i):
    '''
    This constraint calculates the total cost due to the use of Natural Gas to generate 
    thermal energy in the boiler in each scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    foo=[] 
    for c in range (1,model.Classes+1): 
        for f in range(1,model.Periods+1):
            foo.append((i,c,f))
    return  model.Scenario_Lost_Load_Cost_Th[i] == sum(((sum(model.Lost_Load_Th[i,c,t]*model.Value_Of_Lost_Load*model.Delta_Time for i,c,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
 
      
def Initial_Inversion(model):
    '''
    This constraint calculates the initial inversion for the system. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Initial_Inversion == (model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Delta_Time + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost + model.SC_Financial_Cost + model.Tank_Financial_Cost + model.Boiler_Financial_Cost + model.Resistance_Financial_Cost )*(1-model.Porcentage_Funded) 
                                                                 
def Operation_Maintenance_Cost(model):
    '''
    This funtion calculates the operation and maintenance for the system. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Operation_Maintenance_Cost == sum(((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity*model.Maintenance_Operation_Cost_PV + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Delta_Time*model.Maintenance_Operation_Cost_Battery + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost*model.Maintenance_Operation_Cost_Generator + model.SC_Financial_Cost*model.Maintenance_Operation_Cost_SC + model.Tank_Financial_Cost*model.Maintenance_Operation_Cost_Tank + model.Boiler_Financial_Cost*model.Maintenance_Operation_Cost_Boiler + model.Resistance_Financial_Cost*model.Maintenance_Operation_Cost_Resistance)/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 

def Total_Finalcial_Cost(model):
    '''
    This funtion calculates the total financial cost of the system. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''    
    return model.Total_Finalcial_Cost == sum((model.Cost_Financial/((1+model.Discount_Rate)**model.Project_Years[y])) for y  in model.years) 
    
def Battery_Reposition_Cost(model):
    '''
    This funtion calculates the reposition of the battery after a stated time of use. 
    
    :param model: Pyomo model as defined in the Model_creation library.
    ''' 
    return model.Battery_Reposition_Cost == (model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Delta_Time)/((1+model.Discount_Rate)**model.Battery_Reposition_Time)

def Scenario_Net_Present_Cost(model, i): 
    '''
    This function computes the Net Present Cost for the life time of the project, taking in account that the 
    cost are fix for each year.
    
    :param model: Pyomo model as defined in the Model_creation library.
    '''            
    return model.Scenario_Net_Present_Cost[i] == model.Initial_Inversion + model.Operation_Maintenance_Cost + model.Total_Finalcial_Cost + model.Battery_Reposition_Cost + model.Scenario_Lost_Load_Cost[i] + model.Scenario_Lost_Load_Cost_Th[i] + model.Diesel_Cost_Total[i] + model.NG_Cost_Total[i]
                